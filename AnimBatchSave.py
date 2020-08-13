import pymel.core
import os

start_time = pymel.core.playbackOptions(q = True, min = True)
end_time = pymel.core.playbackOptions(q = True, max = True)

def create_reference(file_path):
    if not os.path.exists(file_path):
        
        pymel.core.error("File does not exist: {0}".format(file_path))
        return
    file_path_dir, file_path_fullname = os.path.split(file_path)
    file_path_name, file_path_ext = os.path.splitext(file_path_fullname)
    if "_" in file_path_name:
        file_path_name = "anim"
    pymel.core.createReference(file_path, namespace = file_path_name)

def get_joints_from_namespace(ns):
    return pymel.core.ls("{0}:*".format(ns), type = "joint")  
    
def get_joint_name(ns_and_joint):
    ns, joint_name = ns_and_joint.split(":")
    return joint_name  

def set_start_frame():
    keyframes = pymel.core.keyframe("anim:Hips", q = True)
    start_time = pymel.core.playbackOptions(min = keyframes[0], e = True)
    end_time = pymel.core.playbackOptions(max = keyframes[-1], e = True)
    pymel.core.currentTime(keyframes[0])

def connect_joints(char_joints, anim_joints):
    for c in char_joints:
        c_joint_name = get_joint_name(c)
        for a in anim_joints:
            a_joint_name = get_joint_name(a)
            if c_joint_name == a_joint_name:
                pymel.core.parentConstraint("anim:" + a_joint_name, "character:" + c_joint_name, mo = True)

def create_new_scene():
    pymel.core.newFile(f = True)

def bring_in_char(char_path):
    create_reference(char_path)
    return get_joints_from_namespace("character")

def bring_in_anim(anim_dir, anim_number):
    str_anim_number = str(anim_number).zfill(2)
    anim_path = "{0}/AAA_0{1}0_tk01.ma".format(anim_dir, str_anim_number)
    create_reference(anim_path)
    return anim_path, get_joints_from_namespace("anim")

def remove_anim_reference():
    references = pymel.core.listReferences(parentReference=None, recursive=False, namespaces=False, refNodes=False, references=True)
    pymel.core.system.FileReference.remove(references[1])                      
                       
def save_file(save_dir, anim_number):
    str_anim_number = str(anim_number).zfill(2)
    renamed_file = "{0}/SavedCharAnim_v{1}.mb".format(save_dir, str_anim_number)
    pymel.core.renameFile(renamed_file)
    pymel.core.saveFile(f = True)      


def run_batch(char, anim_dir, save_dir):
    anim_number = 1
    number_of_files = 10
    while anim_number <= number_of_files:
        print "saving file {0}".format(anim_number)
        create_new_scene()
        char_joints = bring_in_char(char)
        anim_path, anim_joints = bring_in_anim(anim_dir, anim_number)
    
        # attach animation to character
        set_start_frame()
        connect_joints(char_joints, anim_joints)

        pymel.core.select(cl = True)
        pymel.core.select(char_joints)
        pymel.core.viewFit(f = .8)
        
        pymel.core.bakeResults(  char_joints,
                                 simulation = True,
                                 time = (start_time, end_time),
                                 sampleBy = 1,
                              )
    
        remove_anim_reference()
        save_file(save_dir, anim_number)
        
        anim_number += 1
 
