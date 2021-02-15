'''
Author - Kaitlyn Behrens
Date - 1/30/2021

This tool applies a batch of motion capture animation to a given character and
saves each as a new file. After saving the final file, it will open a new file.

Place this file in your Maya scripts folder (Documents/Maya/<Maya_Version>), and use
AnimBatchSaveUI to run it.

'''

# Import statements
import pymel.core
import os


# Create a reference to a given file path
def create_reference(file_path, ns):

    # Throw error if file does not exist
    if not os.path.exists(file_path):
        pymel.core.error("File does not exist: {0}".format(file_path))
        return

    # Reference the file and set the namespace 
    pymel.core.createReference(file_path, namespace = ns)



# Create a list of joints that exist for a given namespace
def get_joints_from_namespace(ns):
    return pymel.core.ls("{0}:*".format(ns), type = "joint")
    


# Create the namespace for a given file path
def create_file_namespace(file_path):

    # Split the file path into the file directory and the full file name
    file_dir, file_full_name = os.path.split(file_path)

    # Split the full file name into the name and the extension
    file_name, file_ext = os.path.splitext(file_full_name)

    return file_name



# Create a list of joints that the source and destination skeletons don't have in common   
def get_namespace_diff_list(src_list, dst_list):

    # List joints in the source skeleton and list joints in the destination skeleton
    src_list = [item.split(":")[-1] for item in src_list] 
    dst_list = [item.split(":")[-1] for item in dst_list]

    # Make a list of joint names they do not share
    diff_list = list(set(dst_list) - set(src_list))

    return diff_list
    


# Connect the animation from the source skeleton to the destination skeleton
def connect_anim(src, dst, src_ns, dst_ns):

    # Make a list of joints the two skeletons don't have in common
    diff_list = get_namespace_diff_list(src, dst)

    # Skipping any joints found in the diff_list, parent constrain each joint in the skeletons
    for src_joint in src:
        if  src_joint.split(":")[-1] in diff_list:
            continue
        dst_joint = src_joint.replace(src_ns, dst_ns)
        if not pymel.core.objExists(dst_joint):
            continue
        pymel.core.parentConstraint(src_joint, dst_joint, mo = True)



# Bake animation to the rig skeleton
def bake_anim(skeleton):

    # Set start time back to 1
   #pymel.core.playbackOptions(min = 1)

    # Get current start and end time
    start_time = pymel.core.playbackOptions(min = 1)
    end_time = pymel.core.playbackOptions(q = True, max = True)

    # Clear current selection and select the given skeleton
    pymel.core.select(cl = True)
    pymel.core.select(skeleton)
    
    # Bake animation to skeleton
    pymel.core.bakeResults(
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



# Connect an individual animation file to the character
def connect_rig_to_anim(rig_path, anim_path, save_path):
    
    # Open a new file
    pymel.core.newFile(f = True)

    # Set start time to 0
    pymel.core.playbackOptions(min = 0)
    pymel.core.currentTime(0)

    # Create the namespaces for both the rig and animation files to be referenced in with
    rig_ns = create_file_namespace(rig_path)
    anim_ns = create_file_namespace(anim_path)

    # Create references for both the rig and animation files
    create_reference(rig_path, rig_ns)
    create_reference(anim_path, anim_ns)

    # Create list of joints for both the rig and animation
    rig_skeleton = get_joints_from_namespace(rig_ns)
    anim_skeleton = get_joints_from_namespace(anim_ns)

    # Connect the animation from the anim_skeleton to the rig
    connect_anim(anim_skeleton, rig_skeleton, anim_ns, rig_ns)

    # Bake animation to the rig skeleton
    bake_anim(rig_skeleton)

    # Remove the animation file reference
    anim = pymel.core.system.FileReference(anim_path)
    anim.remove()

    # Throw error if the file save name already exists
    if os.path.exists(save_path):
        pymel.core.error("File name already exists: {0}".format(save_path))
        return

    # Save the file and open a new one
    pymel.core.saveAs(save_path, f = True)
    pymel.core.newFile(f = True)



# Batch save all animation files to the character
def connect_rig_to_anims(rig_path, anim_dir, save_dir):

    # Create a save directory if it doesn't already exist
    if not os.path.exists(save_dir):
        os.mkdir(save_dir)

    # Make a list of names of animation files
    _, _, anim_names = next(os.walk(anim_dir))
    anim_names.sort()

    if ".DS_Store" in anim_names:
        anim_names.remove(".DS_Store")

    # Get all files in directory
    anim_files = ["{0}/{1}".format(anim_dir, anim_name) for anim_name in anim_names]
    
    # Loop through all files
    for anim_file in anim_files:

        # If the file is not a maya file, skip it
        if not anim_file.endswith(".mb") and not anim_file.endswith(".ma"):
            continue

        # Generate a save name
        save_name = "Character_{0}".format(os.path.split(anim_file)[-1])
        save_file = "{0}/{1}".format(save_dir, save_name)
       
        # Connect the rig to the animation
        connect_rig_to_anim(rig_path, anim_file, save_file)
