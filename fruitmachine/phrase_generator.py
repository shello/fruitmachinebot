"""Phrase generator."""

from datetime import date
from functools import reduce
from operator import mul
import random
from typing import Iterable, TypeVar

from .fruitmachine import FruitMachine, MachineStyle, Reel

TemplateLeaf = str
TemplateTree = Iterable
Template = TypeVar('Template', TemplateLeaf, TemplateTree)
TemplateList = Iterable[Template]


class PhraseGenerator:
    """A phrase generator."""

    templates: list

    def __init__(self, templates: Iterable[Template]):
        """Initialise the phrase generator."""
        self.templates = templates

    @classmethod
    def is_template_leaf(cls, template: Template) -> bool:
        """Check if a given template is a "leaf" template."""
        return isinstance(template, str)

    @classmethod
    def template_weight(cls, template: Template, root: bool = False) -> int:
        """Get the weigh of a given template."""
        if cls.is_template_leaf(template):
            return 1

        # Recursively check all the template's sub-parts
        weight_gen = (cls.template_weight(t) for t in template)

        if root:
            return reduce(mul, weight_gen, 1)

        return sum(weight_gen)

    @classmethod
    def get_template_weights(cls, templates: TemplateList,
                             root: bool = False) -> Iterable:
        """Calculate weighs for the templates, in order."""
        return [cls.template_weight(t, root=root) for t in templates]

    @classmethod
    def weighted_choice(cls, templates: TemplateTree,
                        root: bool = False) -> Template:
        """Return a weighted choice between all templates in the tree."""
        return random.choices(templates, k=1,
                              weights=cls.get_template_weights(templates,
                                                               root=root))[0]

    @classmethod
    def instantiate_template(cls, template: Template,
                             root: bool = False) -> str:
        """Turn a template-tree into a template-string."""
        if cls.is_template_leaf(template):
            return template

        if root:
            # The root template concatenates its parts
            return ''.join(cls.instantiate_template(t) for t in template)

        selected_template = cls.weighted_choice(template, root=root)
        return cls.instantiate_template(selected_template)

    def generate_phrase(self, machine: MachineStyle,
                        reels: Iterable[Reel]) -> str:
        """Get a random status."""
        # Prepare parameters for templates
        payline = tuple(FruitMachine.get_description(r[1].description)
                        for r in reels)
        outside_payline = [FruitMachine.get_description(r[0].description)
                           for r in reels] \
            + [FruitMachine.get_description(r[2].description) for r in reels]

        params = {
            'machine': machine.description,
            'payline': payline,
            'random_payline': random.choice(payline),
            'outside_payline': outside_payline,
            'random_outside_payline': random.choice(outside_payline),
            'month': format(date.today(), "%B"),
            'weekday': format(date.today(), "%A")
        }

        selected_template = self.weighted_choice(self.templates)
        template = self.instantiate_template(selected_template, root=True)
        return template.format(**params)
