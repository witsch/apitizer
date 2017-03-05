from rope.base.project import Project
from rope.base.fscommands import FileSystemCommands
from rope.contrib import generate
from rope.refactor import rename, move, change_signature


def get_function(project, module, name):
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
