"""Phrase generator."""

from datetime import date
from functools import reduce
from operator import mul
from random import SystemRandom
from typing import Iterable, Sequence, TypeVar

import inflect

from fruitmachine.parts import MachineStyle, SpunReels

TemplateLeaf = str
TemplateTree = Sequence
Template = TypeVar('Template', TemplateLeaf, TemplateTree)
TemplateList = Sequence[Template]


class PhraseGenerator:
    """A phrase generator."""

    templates: list
    random: SystemRandom

    def __init__(self, templates: Iterable[Template]):
        """Initialise the phrase generator."""
        self.templates = list(templates)
        self.random = SystemRandom()

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
                             root: bool = False) -> Sequence[int]:
        """Calculate weighs for the templates, in order."""
        return [cls.template_weight(t, root=root) for t in templates]

    def weighted_choice(self, templates: TemplateTree,
                        root: bool = False) -> Template:
        """Return a weighted choice between all templates in the tree."""
        weights = self.get_template_weights(templates, root=root)
        return self.random.choices(templates, k=1, weights=weights)[0]

    def instantiate_template(self, template: Template,
                             root: bool = False) -> TemplateLeaf:
        """Turn a template-tree into a template-string."""
        if self.is_template_leaf(template):
            return template

        if root:
            # The root template concatenates its parts
            return ''.join(self.instantiate_template(t) for t in template)

        selected_template = self.weighted_choice(template, root=root)
        return self.instantiate_template(selected_template)

    def generate_phrase(self, machine: MachineStyle, reels: SpunReels) -> str:
        """Get a random status."""
        # Prepare parameters for templates
        payline = tuple(r[1].description for r in reels)
        outside_payline = [r[0].description for r in reels] \
            + [r[2].description for r in reels]

        params = {
            'machine': machine.description,
            'payline': payline,
            'random_payline': self.random.choice(payline),
            'outside_payline': outside_payline,
            'random_outside_payline': self.random.choice(outside_payline),
            'month': format(date.today(), "%B"),
            'weekday': format(date.today(), "%A")
        }

        selected_template = self.weighted_choice(self.templates)
        template = self.instantiate_template(selected_template, root=True)

        # Apply english rules to the formatted string (indef. articles,
        # plurals, etc)
        return inflect.engine().inflect(template.format(**params))
