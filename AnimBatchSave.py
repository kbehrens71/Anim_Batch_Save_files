# apply a given animation to a given character and save the file

import maya.cmds
import os

start_time = maya.cmds.playbackOptions(q = True, min = True)
end_time = maya.cmds.playbackOptions(q = True, max = True) 
char_path = "/Users/kaitlynbehrens/Documents/kaitlyn_maya_projects/maya_v2/sample_files/exercise/character.mb"
#anim_path = "/Users/kaitlynbehrens/Documents/kaitlyn_maya_projects/maya_v2/sample_files/exercise/animations/maya/01_0{0}.ma".format(anim_number)
 
       
def create_reference(file_path, ns):
    file_path_dir, file_path_fullname = os.path.split(file_path)
    file_path_name, file_path_ext = os.path.splitext(file_path_fullname)
    if "_" in file_path_name:
        file_path_name = "anim"
    maya.cmds.file(file_path, r = True, ns = file_path_name)
    
def get_joints_from_namespace(ns):
    return maya.cmds.ls("{0}:*".format(ns), type = "joint")
 

def get_joint_name(ns_and_joint):
    ns, joint_name = ns_and_joint.split(":")
    return joint_name
    
def set_start_frame():
    keyframes = maya.cmds.keyframe("anim:Hips", q = True)
    #print keyframes
    #print keyframes[0]
    #print keyframes[-1]
    
    maya.cmds.playbackOptions(min = keyframes[0], e = True)
    maya.cmds.playbackOptions(max = keyframes[-1], e = True)
    maya.cmds.currentTime(keyframes[0])
          
    
def connect_joints(char_joints, anim_joints):
    for c in char_joints:
        c_joint_name = get_joint_name(c)
        for a in anim_joints:
            a_joint_name = get_joint_name(a)
            if c_joint_name == a_joint_name:
                maya.cmds.parentConstraint("anim:" + a_joint_name, "character:" + c_joint_name, mo = True)
 
 
def create_new_scene():
    maya.cmds.file(new = True, force = True)


def bring_in_char():
    char_path = "/Users/kaitlynbehrens/Documents/kaitlyn_maya_projects/maya_v2/sample_files/exercise/character.mb"
    create_reference(char_path, "character")
    return get_joints_from_namespace("character")

def bring_in_anim(anim_number):
    str_anim_number = str(anim_number).zfill(2)
    anim_path = "/Users/kaitlynbehrens/Documents/kaitlyn_maya_projects/maya_v2/sample_files/exercise/animations/maya/01_{0}.ma".format(str_anim_number)
    create_reference(anim_path, "anim")
    return anim_path, get_joints_from_namespace("anim")
                      
                       
def save_file(anim_number):
    str_anim_number = str(anim_number).zfill(2)
    renamed_file = "/Users/kaitlynbehrens/Documents/kaitlyn_maya_projects/maya_v2/sample_files/exercise/saved/SavedCharAnim_v{0}.mb".format(str_anim_number)
    maya.cmds.file(rename = renamed_file)
    maya.cmds.file(save = True, f = True)


def run():
    anim_number = 1
    number_of_files = 10
    while anim_number <= number_of_files:
        create_new_scene()
        char_joints = bring_in_char()
        #print char_joints
        anim_path, anim_joints = bring_in_anim(anim_number)
        #print anim_joints
    
        # attach animation to character
        set_start_frame()
        #print start_time
        #print end_time
        connect_joints(char_joints, anim_joints)
    
        # bake animation
        maya.cmds.select(cl = True)
        maya.cmds.select(char_joints)
        maya.cmds.viewFit(f = .8)
        maya.cmds.bakeResults(  char_joints,
                            simulation = True,
                            time = (start_time, end_time),
                            sampleBy = 1,
                            oversamplingRate = 1,
                            disableImplicitControl = True,
                            preserveOutsideKeys = True,
                            sparseAnimCurveBake = False,
                            removeBakedAnimFromLayer = False,
                            bakeOnOverrideLayer = False,
                            minimizeRotation = True,
                            controlPoints = False,
                            shape = True
                           )
    
        # remove anim file
        maya.cmds.file(anim_path, rr = True, f = True)
        save_file(anim_number)
        
        anim_number += 1

    
run()
  
 
