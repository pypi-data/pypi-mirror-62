import logging
import os
import time
from typing import Any, Text, Dict, List, Optional, Tuple, Set, Union

import re

from sqlalchemy import and_, or_

from rasa.core.actions.action import default_action_names
from rasa.core.domain import Domain
from rasa.core.events import ActionExecuted, UserUttered, SlotSet
from rasa.core.interpreter import RegexInterpreter
from rasa.core.training.dsl import StoryFileReader, StoryParseError
from rasa.core.training.structures import StoryStep
from rasa.nlu.utils import write_to_file
from rasax.community import config, utils
from rasax.community.database import Story
from rasax.community.database import User
from rasax.community.database.service import DbService
from rasax.community.services.domain_service import DomainService
from rasax.community.utils import (
    get_columns_from_fields,
    get_query_selectors,
    query_result_to_dict,
)

logger = logging.getLogger(__name__)


def dump_stories_to_file_system(
    story_service: "StoryService", team: Text = config.team_name
) -> None:
    """Dump Rasa Core stories in database to file."""

    data_filenames = story_service.get_filenames(team)
    for fname in data_filenames:
        path = os.path.join(fname)
        logger.debug(f"Dumping stories to file '{path}'.")
        stories = story_service.fetch_stories(None, filename=fname)
        markdown = story_service.get_stories_markdown(stories)
        write_to_file(path, markdown)


class StoryService(DbService):
    async def get_story_steps(self, story_string: Text) -> List[StoryStep]:
        """Given story md string reads the contained stories.

        Returns a list of StorySteps in the story if the story is valid and
        [] otherwise.
        """

        domain = DomainService(self.session).get_parsed_domain()
        reader = StoryFileReader(domain, RegexInterpreter())
        try:
            # just split on newlines
            lines = story_string.split("\n")
            return await reader.process_lines(lines)
        except (AttributeError, ValueError) as e:
            raise StoryParseError(
                "Invalid story format. Failed to parse "
                "'{}'\nError: {}".format(story_string, e)
            )

    @staticmethod
    def get_stories_markdown(story_cursor) -> str:
        """Concatenate all stories into one string."""

        bulk_content = ""

        for s in story_cursor:
            bulk_content += "{}\n\n".format(s.get("story"))

        if len(bulk_content):
            bulk_content = bulk_content.strip()
            bulk_content += "\n"

        return bulk_content

    async def save_stories(
        self,
        story_string: Text,
        team: Text,
        filename: Optional[Text] = None,
        username: Optional[Text] = None,
        dump_stories: bool = True,
        add_story_items_to_domain: bool = True,
    ) -> List[Optional[Dict[Text, Any]]]:
        """Saves stories from story string as individual stories."""

        if not filename:
            filename = self.assign_filename(team)

        # split up data into blocks (a new StoryStep begins with #)
        # a split on `#` covers stories beginning with either `##` or `#`
        split_story_string = re.split("(\n|^)##?", story_string)

        # blocks are the non-empty entries of `split_story_string`
        blocks = [s for s in split_story_string if s not in ("", "\n")]

        inserted = []

        for b in blocks:
            # we need to add the initial hashes again (##) to
            # mark the beginning of a story block
            story = "".join(("##", b)).strip()

            # Here, we get a list of StorySteps. A StoryStep is a
            # single story block that may or may not contain
            # checkpoints. A story file contains one or more StorySteps
            steps = await self.get_story_steps(story)
            if steps and steps[0].block_name:
                new_story = Story(
                    name=steps[0].block_name,
                    story=story,
                    annotated_at=time.time(),
                    user=username,
                    filename=filename,
                )

                self.add(new_story)

                self.flush()  # flush to get inserted story id
                if add_story_items_to_domain:
                    await self.add_domain_items_for_story(new_story.id)

                inserted.append(new_story.as_dict())

        if inserted:
            if dump_stories:
                self._dump_stories()
            return inserted
        else:
            return []

    def get_filenames(self, team: Text) -> List[Text]:
        """Return a list of all values of `filename`."""

        filenames = (
            self.query(Story.filename)
            .join(User)
            .filter(User.team == team)
            .distinct()
            .all()
        )
        return [f for f, in filenames]

    def assign_filename(self, team: Text) -> Text:
        """Finds the filename of the oldest document in the collection.

        Returns config.default_stories_filename if no filename was found.
        """

        oldest_file = (
            self.query(Story.filename)
            .join(User)
            .filter(User.team == team)
            .order_by(Story.id.asc())
            .first()
        )

        file_name = utils.get_project_directory()
        if oldest_file:
            file_name = file_name / oldest_file[0]
        else:
            file_name = file_name / config.data_dir / config.default_stories_filename

        return str(file_name)

    def _dump_stories(self):
        if utils.should_dump():
            dump_stories_to_file_system(self)

    async def delete_stories(self, team: Text) -> None:
        """Delete all existing stories."""

        to_delete = self.query(Story).join(User).filter(User.team == team).all()
        self.delete_all(to_delete)

    async def save_stories_from_files(
        self,
        story_files: Union[List[Text], Set[Text]],
        team: Text = config.team_name,
        username: Text = config.default_username,
    ) -> List[Optional[Dict[Text, Any]]]:
        """Save stories from `story_files` to database."""

        from rasax.community.initialise import _read_data

        story_blocks = []

        for data, path in _read_data(list(story_files)):
            logger.debug(f"Injecting stories from file '{path}' to database.")
            additional_blocks = await self.save_stories(
                data,
                team,
                path,
                username,
                dump_stories=False,
                add_story_items_to_domain=False,
            )
            story_blocks.extend(additional_blocks)

        await self.add_domain_items_for_stories()

        return story_blocks

    async def replace_stories(
        self,
        story_string: Text,
        team: Text,
        filename: Optional[Text] = None,
        username: Optional[Text] = None,
        dump_stories: bool = False,
    ) -> List[Optional[Dict[Text, Any]]]:
        """Delete all existing and save new stories."""

        await self.delete_stories(team)

        return await self.save_stories(
            story_string, team, filename, username, dump_stories
        )

    def fetch_stories(
        self,
        text_query: Optional[Text] = None,
        field_query: Optional[List[Tuple[Text, bool]]] = None,
        id_query: Optional[List[int]] = None,
        filename: Optional[Text] = None,
        distinct: bool = True,
    ) -> List[Dict[Text, Any]]:
        if text_query:
            query = Story.story.like(f"%{text_query}%")
        else:
            query = True

        if id_query:
            query = and_(query, or_(Story.id == id for id in id_query))

        if filename:
            query = and_(query, Story.filename == filename)

        columns = get_columns_from_fields(field_query)
        stories = self.query(*get_query_selectors(Story, columns)).filter(query)

        if distinct:
            stories = stories.distinct()

        stories = stories.order_by(Story.id.asc()).all()

        if columns:
            results = [query_result_to_dict(s, field_query) for s in stories]
        else:
            results = [t.as_dict() for t in stories]

        return results

    async def visualize_stories(
        self, stories: List[Dict[Text, Any]], domain: "Domain"
    ) -> Text:
        from networkx.drawing.nx_pydot import to_pydot
        from rasa.core.training.visualization import visualize_stories

        lines = [line for story in stories for line in story["story"].split("\n")]

        reader = StoryFileReader(domain, RegexInterpreter())
        parsed_story_steps = await reader.process_lines(lines)

        graph = await visualize_stories(
            parsed_story_steps, domain, output_file=None, max_history=2
        )

        return to_pydot(graph).to_string()

    def fetch_story(self, story_id: Text) -> Optional[Dict[Text, Any]]:
        story = self.query(Story).filter(and_(Story.id == story_id)).first()

        if story is None:
            return None

        return story.as_dict()

    def delete_story(self, _id: Text) -> bool:
        delete_result = self.query(Story).filter(Story.id == _id).delete()

        return delete_result

    async def _fetch_domain_items_from_story(
        self, story_id: Text
    ) -> Optional[Tuple[Set[Text], Set[Text], Set[Text], Set[Text]]]:
        story = self.fetch_story(story_id)

        if not story:
            return None

        steps = await self.get_story_steps(story["story"])
        story_actions = set()
        story_intents = set()
        story_entities = set()
        story_slots = set()
        for step in steps:
            for e in step.events:
                if isinstance(e, ActionExecuted):
                    # exclude default actions
                    if e.action_name not in default_action_names():
                        story_actions.add(e.action_name)
                elif isinstance(e, UserUttered):
                    intent = e.intent
                    entities = e.entities
                    if intent:
                        story_intents.add(intent.get("name"))
                    if entities:
                        entity_names = [e["entity"] for e in entities]
                        story_entities.update(entity_names)
                elif isinstance(e, SlotSet):
                    slot = e.key
                    if slot:
                        story_slots.add(slot)

        return story_actions, story_intents, story_slots, story_entities

    async def fetch_domain_items_from_stories(
        self,
    ) -> Optional[Tuple[Set[Text], Set[Text], Set[Text], Set[Text]]]:
        """Fetch set of actions, intents, slots and entities from all stories.

        Returns a tuple of four sets.
        """

        stories = self.fetch_stories()

        if not stories:
            return None

        story_ids = [s["id"] for s in stories]
        actions = set()
        intents = set()
        slots = set()
        entities = set()
        for _id in story_ids:
            story_events = await self._fetch_domain_items_from_story(_id)
            actions.update(story_events[0])
            intents.update(story_events[1])
            slots.update(story_events[2])
            entities.update(story_events[3])

        return actions, intents, slots, entities

    async def add_domain_items_for_story(
        self, story_id: Union[int, Text], project_id: Text = config.project_name
    ) -> None:
        """Add story items for `story_id` to domain.

        These are actions, intents, slots and entities.
        """

        story_events = await self._fetch_domain_items_from_story(story_id)
        await self._add_story_items_to_domain(project_id, story_events)

    async def add_domain_items_for_stories(
        self, project_id: Text = config.project_name
    ) -> None:
        """Add story items to domain for all stories in database.

        These are actions, intents, slots and entities.
        """

        story_events = await self.fetch_domain_items_from_stories()
        await self._add_story_items_to_domain(project_id, story_events)

    async def _add_story_items_to_domain(self, project_id, story_events):
        from rasax.community.services.domain_service import DomainService

        domain_service = DomainService(self.session)
        domain_service.add_items_to_domain(
            actions=story_events[0],
            intents=story_events[1],
            slots=story_events[2],
            entities=story_events[3],
            project_id=project_id,
            dump_data=False,
            origin="stories",
        )

    async def update_story(
        self, _id: Text, story_string: Text, user: Dict[Text, Any]
    ) -> Optional[Dict[Text, Any]]:
        story_steps = await self.get_story_steps(story_string)
        if story_steps:
            story = self.query(Story).filter(Story.id == _id).first()

            if story:
                story.user = user["username"]
                story.annotated_at = time.time()
                story.name = story_steps[0].block_name
                story.story = story_string.strip()

                self._dump_stories()

                await self.add_domain_items_for_story(_id)

                return story.as_dict()

        return None
