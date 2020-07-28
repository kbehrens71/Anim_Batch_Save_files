# apply a given animation to a given character and save the file
import maya.cmds
import os
    
       
def create_reference(file_path, ns):
    file_path_dir, file_path_fullname = os.path.split(file_path)
    file_path_name, file_path_ext = os.path.splitext(file_path_fullname)
    if "_" in file_path_name:
        file_path_name = "anim"
    maya.cmds.file(file_path, r = True, ns = file_path_name)
    
def get_joints_from_namespace(ns):
    return maya.cmds.ls("{0}:*".format(ns), type = "joint")
        
   
anim_joints = get_joints_from_namespace("anim")
char_joints = get_joints_from_namespace("character")

rt_x_correction = -180
rt_y_correction = 70
rt_z_correction = 90

lf_y_correction = -70
lf_z_correction = -90


def get_joint_name(ns_and_joint):
    ns, joint_name = ns_and_joint.split(":")
    return joint_name
    
def connect_joints():
    for c in char_joints:
        c_joint_name = get_joint_name(c)
        for a in anim_joints:
            a_joint_name = get_joint_name(a)
            if c_joint_name == a_joint_name:
                if "Hips" in c_joint_name:
                    maya.cmds.parentConstraint("anim:" + a_joint_name, "character:" + c_joint_name)
                elif "Right" in c_joint_name:
                    if "Leg" in c_joint_name:
                        maya.cmds.orientConstraint("anim:" + a_joint_name, "character:" + c_joint_name, o = (rt_x_correction, 0, rt_z_correction))
                    elif "Foot" in c_joint_name:
                        maya.cmds.orientConstraint("anim:" + a_joint_name, "character:" + c_joint_name, o = (rt_x_correction, rt_y_correction, rt_z_correction))
                    else:
                        maya.cmds.orientConstraint("anim:" + a_joint_name, "character:" + c_joint_name, o = (rt_x_correction, 0, 0))
                elif "Left" in c_joint_name:
                    if "Leg" in c_joint_name:
                        maya.cmds.orientConstraint("anim:" + a_joint_name, "character:" + c_joint_name, o = (0, 0, lf_z_correction))
                    elif "Foot" in c_joint_name:
                        maya.cmds.orientConstraint("anim:" + a_joint_name, "character:" + c_joint_name, o = (0, lf_y_correction, lf_z_correction))
                    else:
                        maya.cmds.orientConstraint("anim:" + a_joint_name, "character:" + c_joint_name)
                else: 
                    maya.cmds.orientConstraint("anim:" + a_joint_name, "character:" + c_joint_name)
 
 
           
# create new scene
maya.cmds.file(new = True, force = True)
maya.cmds.playbackOptions( minTime='0sec', maxTime='10sec')
start_time = maya.cmds.playbackOptions(q = True, min = True)
end_time = maya.cmds.playbackOptions(q = True, max = True)
anim_number = 5

# bring in character
char_path = "/Users/kaitlynbehrens/Documents/kaitlyn_maya_projects/maya_v2/sample_files/exercise/character.mb"
create_reference(char_path, "character")

# bring in animation
anim_path = "/Users/kaitlynbehrens/Documents/kaitlyn_maya_projects/maya_v2/sample_files/exercise/animations/maya/01_0{0}.ma".format(anim_number)
create_reference(anim_path, "anim")

# attach animation to character
maya.cmds.parentConstraint("anim:Hips", "character:Reference")
connect_joints()

# bake animation onto joints
maya.cmds.select(cl = True)
maya.cmds.select(char_joints)
maya.cmds.viewFit(f = .8)
maya.cmds.bakeResults(
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
maya.cmds.file( anim_path, rr = True )                       
                       
# save file
renamed_file = "/Users/kaitlynbehrens/Documents/kaitlyn_maya_projects/maya_v2/scenes/sample_files/exercise/saved/SavedCharAnim_v{0}.mb".format(anim_number)
    
maya.cmds.file(rename = renamed_file)
maya.cmds.file(save = True, f = True)

