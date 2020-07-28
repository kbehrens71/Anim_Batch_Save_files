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
    
def connect_joints():
    for c in char_joints:
        c_joint_name = get_joint_name(c)
        for a in anim_joints:
            a_joint_name = get_joint_name(a)
            if c_joint_name == a_joint_name:
                if "Hips" in c_joint_name:
                    #print "parent {0} and {1}".format("anim:" + a_joint_name, "character:" + c_joint_name)
                    maya.cmds.parentConstraint("anim:" + a_joint_name, "character:" + c_joint_name)
                elif ("Leg" in c_joint_name) or ("Foot" in c_joint_name):
                    maya.cmds.orientConstraint("anim:" + a_joint_name, "character:" + c_joint_name, mo = True)
                else:
                    #print "orient {0} and {1}".format("anim:" + a_joint_name, "character:" + c_joint_name) 
                    maya.cmds.orientConstraint("anim:" + a_joint_name, "character:" + c_joint_name)
           
# create new scene
maya.cmds.file(new = True, force = True)
maya.cmds.playbackOptions( minTime='0sec', maxTime='30sec')
#maya.cmds.panZoom(z = 0.1)
anim_number = 1
start_time = 1
end_time = 600

# bring in character
char_path = "/Users/kaitlynbehrens/Documents/kaitlyn_maya_projects/maya_v2/scenes/sample_files/exercise/character.mb"
create_reference(char_path, "character")


# bring in animation
anim_path = "/Users/kaitlynbehrens/Documents/kaitlyn_maya_projects/maya_v2/scenes/sample_files/exercise/animations/maya/01_0{0}.ma".format(anim_number)
create_reference(anim_path, "anim")


# attach animation to character
maya.cmds.parentConstraint("anim:Hips", "character:Reference")
connect_joints()

# bake animation onto joints
maya.cmds.select(cl = True)
maya.cmds.select(char_joints)
maya.cmds.viewFit(f = .7)
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
