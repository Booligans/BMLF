from pybuilder.core import use_plugin, init

use_plugin("python.core")
use_plugin("python.unittest")
use_plugin("python.coverage")
use_plugin("python.distutils")

default_task="publish"

@init
def initialize(project):
    project.set_property("coverage_break_build", False)

