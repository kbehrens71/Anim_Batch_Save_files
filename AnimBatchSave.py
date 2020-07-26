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

def get_joint_name(ns_and_joint):
    ns, joint_name = ns_and_joint.split(":")
    return joint_name

def match_joints():
    for c in char_joints:
        c_joint_name = get_joint_name(c)
        for a in anim_joints:
            a_joint_name = get_joint_name(a)
            if c_joint_name == a_joint_name:
                if "Hips" in c_joint_name:
                    print "parent {0} and {1}".format("anim:" + a_joint_name, "character:" + c_joint_name)
                    maya.cmds.parentConstraint("anim:" + a_joint_name, "character:" + c_joint_name)
                elif ("Leg" in c_joint_name) or ("Foot" in c_joint_name):
                    maya.cmds.orientConstraint("anim:" + a_joint_name, "character:" + c_joint_name, mo = True)
                else:
                    print "orient {0} and {1}".format("anim:" + a_joint_name, "character:" + c_joint_name) 
                    maya.cmds.orientConstraint("anim:" + a_joint_name, "character:" + c_joint_name)
           


# create new scene
maya.cmds.file(new = True, force = True)
anim_number = 1
char_path = "/Users/kaitlynbehrens/Documents/kaitlyn_maya_projects/maya_v2/scenes/sample_files/exercise/character.mb"
anim_path = "/Users/kaitlynbehrens/Documents/kaitlyn_maya_projects/maya_v2/scenes/sample_files/exercise/animations/maya/01_0{0}.ma".format(anim_number)

# bring in character
create_reference(char_path, "character")

# bring in animation
create_reference(anim_path, "anim")

# attach animation to character
maya.cmds.parentConstraint("anim:Hips", "character:Reference")
match_joints()

# bake animation onto joints
#start_time = maya.cmds.playbackOptions(q = True, min = True)
#end_time = maya.cmds.playbackOptions(q = True, max = True)
start_time = 1
end_time = 400

print start_time
print end_time
maya.cmds.select(cl = True)
maya.cmds.select(char_joints)
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
                       
# save file

for i in anim_joints:
    print i
    
for j in char_joints:
    print j
