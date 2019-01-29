# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

# <pep8 compliant>

import bpy
import subprocess

def ShowMessageBox(message = "", title = "PBD JSON Exporting", icon = 'INFO'):
    message = str(message).replace("\\t", "   ").replace("\t", "   ").replace("\\n", "\n")
    def draw(self, context):
        for m in message.splitlines():
            self.layout.label(m)
    bpy.context.window_manager.popup_menu(draw, title = title, icon = icon)

def save(self, context,
         export_type="0",
         input_path="",
         output_path="",
         asset_root="",
         script_path=False,
         precision=5
         ):

    if not script_path:
        ShowMessageBox("The obj to json conversion script path is not set in the addon preferences", "Cannot export json", 'ERROR')
        return False

    param = ["node", script_path, "-t", str(precision), "-CamvDP", "-i", input_path]

    if export_type is "1":
        param.append("--shift-origin")
        param.append("0,span,0")
    if export_type is "2":
        param.append("--set-origin")
        param.append("0,null,0")
        param.append("--shift-origin")
        param.append("null,span,0")

    popenobj = subprocess.Popen(param, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    err = ""
    out = ""

    while not popenobj.poll():
        stderrdata = popenobj.stderr.readline()
        if stderrdata:
            print(str(stderrdata))
            err += stderrdata.decode("UTF-8")
            continue

        stdoutdata = popenobj.stdout.readline()
        if stdoutdata:
            out += stdoutdata.decode("UTF-8")
        else:
            break

    if not err.isspace():
        ShowMessageBox(err+"\n"+out, "Unable to run obj to json script", "ERROR")
        return False

    ShowMessageBox(out, "Batten mesh output", "INFO")
    return True