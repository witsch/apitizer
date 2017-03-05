from functools import partial
from rope.base.project import Project
from rope.base.fscommands import FileSystemCommands
from rope.contrib import generate
from rope.refactor import rename, move, change_signature


def get_function(project, qualifier):
    module, name = qualifier.rsplit('.', 1)
    mod = project.get_module(module)
    offset = mod.source_code.index('def {}('.format(name)) + len('def ')
    return mod.resource, offset


def get_child(resource, name):
    if resource.has_child(name):
        return resource.get_child(name)


def create_module(project, name, package='plone.api', folder='.fakemodules'):
    parent = get_child(project.root, folder) or project.root.create_folder(folder)
    for pkg in package.split('.'):
        parent = get_child(parent, pkg) or generate.create_package(
            project=None, name=pkg, sourcefolder=parent)
    return get_child(parent, name + '.py') or generate.create_module(
        project=None, name=name, sourcefolder=parent)


def main():
    # set up project & fake `plone.api`
    project = Project('.', fscommands=FileSystemCommands())
    portal = create_module(project, name='portal')
    get_func = partial(get_function, project)
    move_func = lambda func: move.create_move(project, *get_func(func))
    rename_func = lambda func: rename.Rename(project, *get_func(func))
    do = project.do

    # replace `getToolByName`
    func = get_func('Products.CMFCore.utils.getToolByName')
    signature = change_signature.ChangeSignature(project, *func)
    do(signature.get_changes([change_signature.ArgumentRemover(0)]))
    do(move_func('Products.CMFCore.utils.getToolByName').get_changes(portal))
    do(rename_func('plone.api.portal.getToolByName').get_changes('get_tool'))

    # clean up
    project.close()
