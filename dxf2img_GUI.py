import matplotlib.pyplot as plt
import ezdxf
from ezdxf.addons.drawing import RenderContext, Frontend
from ezdxf.addons.drawing.matplotlib import MatplotlibBackend
import wx
import glob
import re


class DXF2IMG(object):

    default_img_format = '.png'
    default_img_res = 300
    def convert_dxf2img(self, names, img_format=default_img_format, img_res=default_img_res):
        for name in names:
            doc = ezdxf.readfile(name)
            msp = doc.modelspace()
            # Recommended: audit & repair DXF document before rendering
            auditor = doc.audit()
            # The auditor.errors attribute stores severe errors,
            # which *may* raise exceptions when rendering.
            if len(auditor.errors) != 0:
                raise exception("The DXF document is damaged and can't be converted!")
            else :
                fig = plt.figure()
                ax = fig.add_axes([0, 0, 1, 1])
                ctx = RenderContext(doc)
                ctx.set_current_layout(msp)
                ctx.current_layout.set_colors(bg='#FFFFFF')
                out = MatplotlibBackend(ax)
                Frontend(ctx, out).draw_layout(msp, finalize=True)

                img_name = re.findall("(\S+)\.",name)  # select the image name that is the same as the dxf file name
                first_param = ''.join(img_name) + img_format  #concatenate list and string
                fig.savefig(first_param, dpi=img_res)


#================================================================================================

user_files = list()
reso = ''
formats = ''
class The_GUI(wx.Frame):

    def __init__(self):
        super().__init__(None, title='DXf Converter', size=(400,350),     #define the frame
                        style=wx.MINIMIZE_BOX | wx.RESIZE_BORDER | wx.SYSTEM_MENU |
                         wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN)

        panel = wx.Panel(self)


        first_static = wx.StaticBox(panel, label='Folder Selection',
                            size=(370,200),pos=(5,5))

        self.list_ctrl = wx.ListCtrl(
            panel, size=(-1, 100),name='first_list',
            style=wx.LC_REPORT | wx.BORDER_SUNKEN,
            pos=(20,30))
        self.list_ctrl.InsertColumn(0, 'DXFS', width=300)

        font1 = wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.DEFAULT)
        st1 = wx.StaticText(panel, label='Type Or Select Folder :',
                    style=wx.ALIGN_LEFT, pos=(20,140))
        st1.SetFont(font1)



        self.rtb = wx.TextCtrl(panel,style=wx.TE_PROCESS_ENTER,
                                pos=(20,163),size=(199,25))
        user_folder1 = self.rtb.Bind(wx.EVT_TEXT_ENTER, self.Txt_Ent, id = -1)



        folder_btn = wx.Button(panel,label='Select Folder',pos=(270,166))
        folder_btn.Bind(wx.EVT_BUTTON,self.on_open_folder)

#=============================================================================

        second_static = wx.StaticBox(panel, label='Output',
                        size=(370,150),pos=(5,210))


        font2 = wx.Font(9, wx.DEFAULT, wx.NORMAL, wx.DEFAULT)
        st2 = wx.StaticText(panel, label='Image Format :',
                            style=wx.ALIGN_LEFT, pos=(13,250))
        st2.SetFont(font2)

        formats = ['.png','.pdf','.jpg','.tiff']
        formats_cb = wx.ComboBox(panel, pos=(107, 250), choices=formats,
            style=wx.CB_READONLY)
        formats_cb.Bind(wx.EVT_COMBOBOX, self.on_select_fcb)

        st3 = wx.StaticText(panel, label='Resolution :',
                            style=wx.ALIGN_LEFT, pos=(180,250))
        st3.SetFont(font2)
        reso = ['1080','720','480']
        reso_cb = wx.ComboBox(panel, pos=(257, 250), choices=reso,
                            style=wx.CB_READONLY)
        reso_cb.Bind(wx.EVT_COMBOBOX,self.on_select_rcb)

        convert_btn = wx.Button(panel, label='Convert Files',pos=(270,280))
        convert_btn.Bind(wx.EVT_BUTTON,self.on_convert)

        font3 = wx.Font(7, wx.DEFAULT, wx.NORMAL, wx.DEFAULT)
        help_tag = wx.StaticText(panel, label='Help:hamzahamza050875@gmail.com',
                                style=wx.ALIGN_LEFT, pos=(3,297))
        help_tag.SetFont(font3)

        self.Show()

#============================================================================
    def update_dxf_listing(self, folder_path):
        self.current_folder_path = folder_path
        """
        this function look for the paths of the dxf file using glob
        the folder_path parm : for the folder
        """
        dxfs = glob.glob(folder_path + '/*.dxf')    #this search for the dxf in the folder_path
        if dxfs == [] :
             wx.MessageBox('No DXF files were found in this file', 'Not Found', wx.OK | wx.ICON_ERROR)
        names = []
        index = 0

        for dxf in dxfs:
            user_files.append(dxf)

        for name in user_files :
            self.list_ctrl.InsertItem(index, name)
            index += 1


    def Txt_Ent(self,event):
        user_folder1 = (str(self.rtb.GetValue()))
        self.update_dxf_listing(user_folder1)



    def on_open_folder(self, event):
        title = "Choose a directory:"
        dlg = wx.DirDialog(self, title,style=wx.DD_DEFAULT_STYLE)

        if dlg.ShowModal() == wx.ID_OK:
            user_folder2 = dlg.GetPath()
            self.update_dxf_listing(user_folder2)
        dlg.Destroy()


    def on_select_fcb(self,event):
        formats = event.GetString()

    def on_select_rcb(self,event):
        reso = event.GetString()


    def on_convert(self, event):
        first =  DXF2IMG()
        first.convert_dxf2img(user_files,img_format=formats)


if __name__ == '__main__':
    app = wx.App()
    frame = The_GUI()
    app.MainLoop()
    print(formats)
