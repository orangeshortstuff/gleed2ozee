import xml.etree.ElementTree as ET
import os, sys, time

def import_from_gleed(filename: str):
    global start_time, end_time
    start_time = time.perf_counter_ns()
    tree = ET.parse(filename)
    root = tree.getroot()

    layers = [] # layers to search through for items
    items = [] # items to turn into properties
    item_structs = [] # resulting structs

    pixels_per_unit = 105 # 1x scale rock texture = 4 units
    size_factor = 420 / pixels_per_unit # scale between ozee and gleed units
    #note to self: make sure the root folder is always the textures folder

    for child in root[0]: # get layers only
        #print(child.attrib["Name"])
        layers.append(child)

    for layer in layers[0]: # items
        for item in layer:
            if item.tag == "Item": # leave out the x and y scroll
                items.append(item)

    for item in items: # get item attributes
        struct = []
        static = True
        struct.append(item.attrib["Name"]) # name of the item
        temp_scale = [1,1]
        tags = [prop.tag for prop in item]
        # print(tags)
        if "Position" in tags: # look for a position tag
            idx = tags.index("Position") # get the index
            # split into x and y position, and append
            struct.append([round(int(item[idx][0].text) / pixels_per_unit, 2),
                            round(int(item[idx][1].text) / pixels_per_unit, 2)]) 
        else:
            print("no position found")

        if "Rotation" in tags: # look for a position tag
            idx = tags.index("Rotation") # get the index
            # split into x and y position, and append
            struct.append(round(float(item[idx].text), 2)) 
        else:
            struct.append(0.0)
            #print("no rotation found")

        if "asset_name" in tags: # search for asset name
            idx = tags.index("asset_name")
            #print(idx, item[idx].text)
            struct.append(item[idx].text) # texture name becomes the type

            if "Scale" in tags:
                idx = tags.index("Scale")
                # print(idx, item[idx][0].text, item[idx][1].text)
                # convert to ozee units
                temp_scale = [float(item[idx][0].text) * size_factor,
                            float(item[idx][1].text) * size_factor]
            else:
                print("no scale found")

        else: # we're dealing with a primitive (rectangle / circle)
            #print("no texture found")

            if "Height" in tags and "Width" in tags: # rectangle case
                struct.append("rectangle")
                idx = tags.index("Width")
                idx2 = tags.index("Height")
                # print(idx, item[idx][0].text, item[idx][1].text)
                # convert to ozee units
                temp_scale = [round(float(item[idx].text) / pixels_per_unit, 2),
                            round(float(item[idx2].text) / pixels_per_unit, 2)]
                # center position of the item
                struct[1][0] += temp_scale[0] / 2
                struct[1][0] = round(struct[1][0], 2)
                struct[1][1] += temp_scale[1] / 2
                struct[1][1] = round(struct[1][1], 2)
                
            else:
                if "Radius" in tags: # circle case
                    struct.append("circle")
                    idx = tags.index("Radius")
                    # print(idx, item[idx][0].text, item[idx][1].text)
                    # convert to ozee units
                    temp_scale = round(float(item[idx].text) / pixels_per_unit, 2)
                else:
                    print("no scale found")
        
        struct.append(temp_scale)
        item_structs.append(struct)

    end_time = time.perf_counter_ns()
    
    for struct in item_structs:
        #print(struct)
        pass

    return item_structs

def export_to_ozee(objects, filename: str):
    scaleable_objects = ["Ice","Rock","Wood","Rubber", "Spikes", "Rectangle", "Circle"]
    materials = scaleable_objects[:4]
    fstart_time = time.perf_counter_ns()
    try:
        with open(filename, "x") as f: # create new file if it doesn't exist
            pass
    except:
        #print("File already exists.")
        pass
    with open(filename, "w") as f: # remove file contents
        pass

    with open(filename, "a") as f: # re-make the map
        # write the header
        f.write("<?xml version=\"1.0\" encoding=\"utf-8\" ?>\n")
        f.write("<map xmin=\"-500\" ymin=\"-100\" xmax=\"1000\" ymax=\"50\" color=\"0x3a554d\" bg=\"assets.background.Forest\">\n")
        f.write("\t<front>\n\n\t</front>\n") # blank front layer
        f.write("\t<middle>\n") # start of middle layer
        back_objs = []
        for obj in objects:
            # structure of an object: name, position, rotation, type, scale
            name = obj[0]
            position = obj[1]
            rotation = obj[2]
            obj_type = obj[3].capitalize()
            scale = obj[4]

            if obj_type in materials: # make a box, and treat the type as a material
                f.write("\t\t<el id=\"" + name + "\" type=\"Box\" material=\"" + obj_type + "\" static=\"true\" x=\""+ 
                        str(position[0]) +"\" y=\"" + str(position[1]) +"\" w=\"" + 
                        str(scale[0]) + "\" h=\"" + str(scale[1]) + "\" a=\"" + str(rotation) + "\" />\n")
                pass
            else:
                if obj_type == "Spikes": # writes width only
                    f.write("\t\t<el id=\"" + name + "\" type=\"Spikes\" static=\"true\" x=\""+ 
                        str(position[0]) +"\" y=\"" + str(position[1]) +"\" w=\"" + 
                        str(scale[0]) + "\" a=\"" + str(rotation) + "\" />\n")
                elif obj_type in scaleable_objects: # non-static object - default to the Ice material
                    if obj_type == "Rectangle":
                        f.write("\t\t<el id=\"" + name + "\" type=\"Box\" material=\"Ice\" static=\"false\" x=\""+ 
                        str(position[0]) +"\" y=\"" + str(position[1]) +"\" w=\"" + 
                        str(scale[0]) + "\" h=\"" + str(scale[1]) + "\" a=\"" + str(rotation) + "\" />\n")
                    elif obj_type == "Circle":
                        f.write("\t\t<el id=\"" + name + "\" type=\"Wheel\" material=\"Ice\" static=\"false\" x=\""+ 
                        str(position[0]) +"\" y=\"" + str(position[1]) +"\" r=\"" + 
                        str(scale) + "\" />\n")
                else: # door, checkpoint, or coin
                    if obj_type == "Coin":
                        f.write("\t\t<el type=\"Coin\" x=\""+ str(position[0]) +"\" y=\"" + str(position[1]) +"\" />\n")
                    elif obj_type == "Button":
                        f.write("\t\t<el id=\"" + name + "\" type=\"ButtonSwitch\" static=\"true\" x=\"" +
                                str(position[0]) +"\" y=\"" + str(round(position[1] + 0.14,2)) + "\" a=\"" + str(rotation) + "\" />\n")
                    elif obj_type == "Lever":
                        f.write("\t\t<el id=\"" + name + "\" type=\"LeverSwitch\" mode=\"ThreeStateSpring\" static=\"true\" x=\"" +
                                str(position[0]) +"\" y=\"" +  str(round(position[1] + 0.5,2)) + "\" a=\"" + str(rotation) + "\" pos=\"Center\" />\n")
                    elif obj_type == "Hang":
                        f.write("\t\t<el id=\"" + name + "\" type=\"HangSwitch\" static=\"true\" x=\"" +
                                str(position[0]) +"\" y=\"" + str(position[1]) + "\" a=\"" + str(rotation) + "\" />\n")
                    elif obj_type == "Door" or obj_type == "Checkpoint":
                        back_objs.append(obj)

        f.write("\t</middle>\n") # end middle layer
        f.write("\t<back>\n")
        for obj in back_objs: # maybe have a pre-parsing phase to not repeat this?
            name = obj[0]
            position = obj[1]
            rotation = obj[2]
            obj_type = obj[3].capitalize()
            scale = obj[4]
            if obj_type == "Door": 
                f.write("\t\t<el type=\"Door\" x=\""+ str(position[0]) +"\" y=\"" + str(round(position[1] + 1.4,2)) +
                        "\" tx=\"0\" ty=\"0\" map=\"Map000\" filter=\"false\" />\n")
            elif obj_type == "Checkpoint":
                f.write("\t\t<el type=\"Checkpoint\" x=\""+ str(position[0]) +"\" y=\"" + str(round(position[1] + 1.3,2)) +"\" />\n")
        f.write("\t</back>\n")
        # close the map
        f.write("</map>")
        pass
    
    fend_time = time.perf_counter_ns()
    print("Exported " + str(len(objects)) + " objects in " + str((end_time - start_time) / 10**6) + " ms")
    print("Wrote to file in " + str((fend_time - fstart_time) / 10**6) + " ms")
    print("Total time: " + str((fend_time - start_time) / 10**6) + " ms")
    return

def main():
    os.chdir(sys.path[0]) # set cwd to current folder
    try:
        with open("auto.txt","r") as f:
            in_file = f.readline()[:-1] # -1 to remove newline
            out_file = f.readline()
    except:
        in_file = input("Gleed file name: ")
        out_file = input("Output file name: ")
        save = input("Save to file? (Y/N) ")[0].upper()
        if save == "Y":
            with open("auto.txt","w") as f:
                f.write(in_file)
                f.write(out_file)
    objects = import_from_gleed(in_file)
    export_to_ozee(objects, out_file)

if __name__ == "__main__":
    main()
