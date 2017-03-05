from rope.base.project import Project
from rope.base.fscommands import FileSystemCommands
from rope.contrib import generate
from rope.refactor import rename, move, change_signature


def get_function(project, module, name):
    mod = project.get_module(module)
    offset = mod.source_code.index('def {}('.format(name)) + len('def ')
    return mod.resource, offset


def main():
    # set up project & fake `plone.api`
    project = Project('.', fscommands=FileSystemCommands())
    fakes = project.root.create_folder('.fakemodules')
    pkg = generate.create_package(None, 'plone', sourcefolder=fakes)
    pkg = generate.create_package(None, 'api', sourcefolder=pkg)
    portal = generate.create_module(None, 'portal', sourcefolder=pkg)

    # replace `getToolByName`
    func = get_function(project, 'Products.CMFCore.utils', 'getToolByName')
    signature = change_signature.ChangeSignature(project, *func)
    project.do(signature.get_changes([change_signature.ArgumentRemover(0)]))
    func = get_function(project, 'Products.CMFCore.utils', 'getToolByName')
    project.do(move.create_move(project, *func).get_changes(portal))
    func = get_function(project, 'plone.api.portal', 'getToolByName')
    project.do(rename.Rename(project, *func).get_changes('get_tool'))

    # clean up
    project.close()
