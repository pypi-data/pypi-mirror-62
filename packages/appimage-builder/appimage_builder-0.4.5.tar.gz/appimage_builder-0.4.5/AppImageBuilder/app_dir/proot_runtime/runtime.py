#  Copyright  2020 Alexis Lopez Zubieta
#
#  Permission is hereby granted, free of charge, to any person obtaining a
#  copy of this software and associated documentation files (the "Software"),
#  to deal in the Software without restriction, including without limitation the
#  rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
#  sell copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in
#  all copies or substantial portions of the Software.
import fnmatch
import logging
import os

from AppImageBuilder.app_dir.metadata.loader import AppInfoLoader
from AppImageBuilder.recipe import Recipe
from .app_run import PRootAppRun
from .helpers.factory import PRootHelperFactory
from ..runtime.helpers.dynamic_loader import DynamicLoaderError
from ..runtime.runtime import Runtime


class PRootRuntime(Runtime):
    def __init__(self, recipe: Recipe):
        super().__init__(recipe)

        self.app_run_constructor = PRootAppRun
        self.helper_factory_constructor = PRootHelperFactory