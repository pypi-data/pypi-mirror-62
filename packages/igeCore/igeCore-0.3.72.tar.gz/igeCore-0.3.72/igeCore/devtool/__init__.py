"""
indi game engine offline develop tools

convert 3d assets
convert images to platform dipend format
make ige package
upload package to devserver

"""

import py_compile
import shutil
import glob
import os.path
import igeCore as core
from igeCore import apputil
from igeCore.devtool._igeTools import *
from igeCore import apputil
from igeCore.apputil import launch_server
import hashlib
import tokenize

FileBehavior = [
    ('.pyxf', 'copy'),
    ('.pyxa', 'copy'),
    ('.pyxb', 'copy'),
    ('.py', 'compile'),
    ('.dae', 'model'),
    ('.png', 'image'),
    ('.dds', 'image'),
    ('.tga', 'image'),
    ('.psd', 'image'),
    ('.json', 'copy'),
    ('.pickle', 'copy'),
    ('.zip', 'copy'),
    ('.txt', 'copy'),
    ('.db', 'copy'),
    ('.ttf', 'copy')
]
def getFileBehavior(file):
    name, ext = os.path.splitext(file)
    for t in FileBehavior:
        if t[0] == ext:
            return t[1]
    return 'skip'

def appendFileBehavior(ext, behavior):
    FileBehavior.append((ext,behavior))

def compileAndCopy(src,dst, allcopy = False):
    """
    Compile  all *.py files in src directory.
	Other files will be copied if allcopy is True, 
	or copy according to FileBehavior if False.
	
	Parameters
	----------
       src : string
           source root folder
       dst: string
           destination root folder
       allcopy : bool
           copy all files except *. py
    """

    def findBuildFiles(path):
        list = []
        for root, dirs, files in os.walk(path):
            if root.find('\.') != -1: continue
            if root == '__pycache__': continue
            for fname in files:
                list.append(os.path.join(root, fname))
        return list
    def replaceExt(file, ext):
        name, extold = os.path.splitext(file)
        return name + ext

    # copy file and compile py
    list = findBuildFiles(src)
    for infile in list:
        type = getFileBehavior(infile)
        if type == 'copy' or (type == 'skip' and allcopy):
            outfile = os.path.normpath(infile.replace(src, dst, 1))
            apputil.makeDirectories(outfile)
            print('copy : '+infile)
            shutil.copy(infile, outfile)

        elif type == 'compile':
            outfile = os.path.normpath(infile.replace(src, dst, 1))
            apputil.makeDirectories(outfile)
            if os.path.basename(infile) == 'root.py':
                shutil.copy(infile, outfile)
            else:
                outfile = replaceExt(outfile, '.pyc')
                apputil.makeDirectories(outfile)
                print('compile : '+infile)
                py_compile.compile(infile, outfile)

def convertAssets(src,dst,platform, unit=1.0):
    """
    Convert model and image data to ige format
    model(.dae) -> .pyxf
    image(.png .dds .tga .psd ) -> .pyxi

    If model data with the same name as the folder name is found,
    it is regarded as base model data, and other model data in the
    same folder are regarded as motion files, and all are packed
    into one file
    If there is no model data with the same name as the folder name,
    Each model data as base model data and convert separately

    

    :param src: source root folder
    :param dst: destination root folder
    :param platform: target platform (core.TARGET_PLATFORM_XX)
    :param unit: scale unit size of 3d model
    :return: None
    """
    def findImages(path):
        list = []
        for root, dirs, files in os.walk(path):
            if root.find('\.') != -1: continue
            for fname in files:
                name, ext = os.path.splitext(fname)
                if ext == '.png' or ext == '.dds' or ext == '.tga' or ext == '.psd':
                    list.append(os.path.join(root, fname))
        return list
    def createDirectoryTree(filelist, root):
        imageDirectory = dict()
        for img in filelist:
            while True:
                img, file = os.path.split(img)
                if img not in imageDirectory:
                    imageDirectory[img] = {file: 0};
                elif file not in imageDirectory[img]:
                    imageDirectory[img][file] = 0
                if img == root: break
        return imageDirectory
    def findFileFromDiorectoryTree(imageDirectory, file, dir):
        files = imageDirectory.get(dir)
        if files is None: return None
        if file in files:
            return os.path.join(dir, file)
        for d in files:
            _, ext = os.path.splitext(d)
            if ext is '':
                rv = findFileFromDiorectoryTree(imageDirectory, file, os.path.join(dir, d))
                if rv: return rv
        return None
    def findConvertSet(path):
        dict = {}
        for root, dirs, files in os.walk(path):
            if root.find('\.') != -1: continue
            folder = os.path.basename(root)
            baseFile = folder + '.dae'

            folderRule = False
            for f in files:
                if f == baseFile:
                    folderRule = True
                    break

            if folderRule:
                daes = [os.path.join(root, baseFile)]
                for f2 in files:
                    f2_name, f2_ext = os.path.splitext(f2)
                    if f2_ext == '.dae' and f2_name != folder:
                        daes.append(os.path.join(root, f2))
                dict[folder] = daes
            else:
                for f2 in files:
                    f2_name, f2_ext = os.path.splitext(f2)
                    if f2_ext == '.dae':
                        dict[f2_name] = [os.path.join(root, f2)]
        return dict
    def removeRoot(path, root):
        newpath = path.replace(root, '', 1)
        if newpath[0] == '/' or newpath[0] == '\\':
            newpath = newpath[1:]
        return newpath
    def replaceExt(file, ext):
        name, extold = os.path.splitext(file)
        return name + ext
    def readAndCalcHash(srcfile, dstfile, hashfile):
        hashcode = '00000000000000000000000000000000'
        newhash  = 'ffffffffffffffffffffffffffffffff'
        if os.path.exists(dstfile):
            try:
                with open(hashfile, 'r') as f:
                    hashcode = f.read()
            except : None

        with open(srcfile, 'rb') as f:
	        fileDataBinary = f.read()
	        if len(fileDataBinary) is not 0:
	            hash = hashlib.md5()
	            hash.update(fileDataBinary)
	            newhash = hash.hexdigest()
        return hashcode,newhash
    def saveHash(hashfile, newhash):
        if newhash != 'ffffffffffffffffffffffffffffffff':
            apputil.makeDirectories(hashfile)
            with open(hashfile, 'w') as f:
                f.write(newhash)
    def readFigureConf(path):
        mode = 0
        label = ''
        keyvalue = {}
        with open(path, 'rb') as f:
            for token in tokenize.tokenize(f.readline):
                if token.type is tokenize.ENDMARKER:
                    break
                elif token.type is tokenize.NAME:
                    if mode is 0:
                        label = token.string
                    else:
                        keyvalue[label] = token.string
                        mode = 0
                elif token.type is tokenize.OP:
                    mode = 1
                elif token.type is tokenize.NUMBER:
                    if mode is 1:
                        try:
                            keyvalue[label] = int(token.string)
                        except ValueError:
                            keyvalue[label] = float(token.string)
                        mode = 0
        return keyvalue
    def createFigureConfTree(path):
        filelist = []
        for root, dirs, files in os.walk(path):
            if root.find('\.') != -1: continue
            for fname in files:
                if fname == 'figure.conf':
                    filelist.append(os.path.join(root, fname))
        figureConfTree = dict()
        for filepath in filelist:
            conf = readFigureConf(filepath)
            dir, file = os.path.split(filepath)
            figureConfTree[dir] = conf

        for dir, val in figureConfTree.items():
            while True:
                dir, _ = os.path.split(dir)
                if len(dir) is 0:
                    break
                parent = figureConfTree.get(dir)
                if parent is not None:
                    for parentkey, parentval in parent.items():
                        if val.get(parentkey) is None:
                            val[parentkey] = parentval
        return figureConfTree
    def findConf(dir: str, tree: dict):
        while True:
            dir, _ = os.path.split(dir)
            if len(dir) is 0:
                break
            conf = tree.get(dir)
            if conf is not None:
                return conf
        return dict()

    confTree = createFigureConfTree(src)
    allimages = findImages(src)
    imageDirectory = createDirectoryTree(allimages, src)
    daes = findConvertSet(src)
    allTextures = dict()
    tmpfig = core.editableFigure("tmpfigure")
    for key, data in daes.items():
        tmpfig.clear()
        conf = findConf(data[0], confTree)
        if conf.get('BASE_SCALE') is None:
           conf['BASE_SCALE'] = unit

        loadCollada(data[0], tmpfig, conf)
        for i in range(1, len(data)):
            loadColladaAnimation(data[i], tmpfig, conf)
        path, file = os.path.split(data[0])

        texs = tmpfig.getTextureSource()
        for tex in texs:
            filename = os.path.basename(tex['path'])
            current = path
            inputimage = None
            while True:
                inputimage = findFileFromDiorectoryTree(imageDirectory,filename, current)
                if inputimage is not None: break
                if current == src: break
                current,_ = os.path.split(current)
            if inputimage is None:
                print('file not found '+ tex['path'])
            else:
                allTextures[inputimage] = tex;
                inputimage = inputimage.replace('\\', '/')
                inputimage = removeRoot(inputimage,src);
                inputimage,ext = os.path.splitext(inputimage)
                newTex = {'path':inputimage, 'normal': tex['normal'], 'wrap': tex['wrap']}
                tmpfig.replaceTextureSource(tex, newTex)

        outfile = os.path.normpath(data[0].replace(src, dst, 1))
        outfile = replaceExt(outfile, '.pyxf')
        apputil.makeDirectories(outfile)
        tmpfig.mergeMesh()
        tmpfig.saveFigure(outfile)

    for img in allimages:
        if img not in allTextures:
            newTex = {'path': removeRoot(img,src), 'normal': False, 'wrap': False}
            allTextures[img] = newTex

    for key, val in allTextures.items():
        outfile = os.path.normpath(key.replace(src, dst, 1))
        outfile = replaceExt(outfile, '.pyxi')
        hashfile = os.path.normpath(key.replace(src, '.tmp/hash', 1))
        hashcode, newhash = readAndCalcHash(key, outfile, hashfile)
        if hashcode != newhash:
            apputil.makeDirectories(outfile)
            convertTextureToPlatform(key, outfile, platform, val['normal'], val['wrap'])
            saveHash(hashfile, newhash)
        else:
            print("skip convert {} because no change".format(key))


def packFolders(root):
    """
    convert folder to indi game engine asset database format
    :param root: convert all folders under root
    :return: None
    """
    list =glob.glob(os.path.join(root,'*' ))
    for dir in list:
        if os.path.isdir(dir):
            compressFolder(dir)

def deploy(projectFolder, userID, appName, appVersion, unit = 1.0):
    """
    Convert all assets to platform dipend format and upload to the ige develop server
    All intermediate files are stored in the '.tmp' folder

    :param projectFolder:  root path of project to convert.
    :param userID:  Your ID
    :param appName:  apprication name
    :param appVersion:  apprication version (don't use period)
    :param unit:  3d model's base scale unit. you can adjust 3d model scale.
    :return:
    """

    def makeProjectDir(user, app, version, platform):
        root = '/'
        if launch_server.mkdir(root, user) == 0:
            root += user
            if launch_server.mkdir(root, app) == 0:
                root += '/'
                root += app
                if launch_server.mkdir(root, version) == 0:
                    root += '/'
                    root += version
                    if launch_server.mkdir(root, apputil.platformName(platform))==0:
                        return True
        return False

    def deployPlatform(platform, projectFolder, userID, appName, appVersion, unit):
        tmp = '.tmp/stage/'+appName+'/'+ apputil.platformName(platform)
        compileAndCopy(projectFolder,tmp)
        convertAssets(projectFolder,tmp,platform,unit);
        packFolders(tmp)
        if makeProjectDir(userID, appName, appVersion, platform) != True:
            return
        addr = '/'+userID+'/'+appName+'/'+str(appVersion)+'/'+ apputil.platformName(platform)
        launch_server.upload_files(tmp, addr)

    deployPlatform(core.TARGET_PLATFORM_PC, projectFolder, userID, appName, appVersion, unit)
    deployPlatform(core.TARGET_PLATFORM_IOS, projectFolder, userID, appName, appVersion, unit)
    deployPlatform(core.TARGET_PLATFORM_ANDROID, projectFolder, userID, appName, appVersion, unit)
