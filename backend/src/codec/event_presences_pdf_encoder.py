from datetime import datetime
from fpdf import FPDF
from PIL import Image
import os


class EventPresencesPdfEncoder(object):

    def __init__(self, event, organizer, drawable_path='../../frontend/res/drawables/', data_path='../data/'):
        self._event = event
        self._organizer = organizer
        self._drawable_path = drawable_path
        self._data_path = data_path
        self._pdf = None
        self._w = 0
        self._th = 0

    def encode(self):
        self._pdf = FPDF()
        self._pdf.set_title('Presences')
        self._w = self._pdf.w - self._pdf.l_margin - self._pdf.r_margin
        self._pdf.add_page()
        self._pdf.set_font("Arial", '', size=12)
        self._pdf.set_draw_color(0, 0, 0)
        self.print_head()
        self._pdf.ln(self._pdf.font_size)
        self.print_attendees()
        self._pdf.set_display_mode('fullpage', 'single')
        p = self._pdf.output(dest='S')
        return p.encode('latin-1')

    def print_head(self):
        self.print_logo()
        self.print_info()

    def print_logo(self):
        logo_path = os.path.join(self._drawable_path, 'mididec.png')
        self._pdf.image(logo_path,
                        x=self._w/2, w=20, h=20)
        self._pdf.ln(self._pdf.font_size*2)

    def print_info(self):
        start = datetime.strptime(self._event.start, "%Y-%m-%dT%H:%M:%SZ")
        self._print_title('Title:', self._event.title)
        self._print_title('Date:', start.strftime("%d %B %Y"))
        self._print_title('Organisateur:', self._organizer.name)

    def _print_title(self, title, value):
        self._pdf.set_font("Arial", 'B', size=15)
        self._pdf.cell(self._w/2, self._pdf.font_size, txt=title, ln=0,
                       border=0,  align="L")
        self._pdf.set_font("Arial", '', size=15)
        self._pdf.cell(self._w/2, self._pdf.font_size, txt=value, border=0,
                       align="L")
        self._pdf.ln(self._pdf.font_size*1.5)

    def print_attendees(self):
        self._pdf.set_font("Arial", '', size=12)
        th = self._pdf.font_size
        self._pdf.ln(th*2)
        maxname = self._calculate_max_namesize()
        imgw = 10
        oiqw = 10
        h = 10
        hm = 5
        wm = 5
        signaturew = self._w - imgw - wm - maxname - wm - oiqw - wm
        self._print_attendees_head(imgw, maxname, signaturew, oiqw, wm)
        self._pdf.set_line_width(0.5)
        offy = self._pdf.y
        offx = self._pdf.x
        di = 0
        i = 0
        y = offy
        self._pdf.set_font("Arial", '', size=12)
        for attendee in self._event.attendees:
            x = offx
            if attendee.avatar_path:
                pdf_path = self._create_png_avatar(attendee.avatar_path)
                self._pdf.image(pdf_path, x=x,
                                y=y, w=imgw, h=h)
            else:
                default_path = os.path.join(self._drawable_path, 'mididec.png')
                self._pdf.image(default_path,
                                x=x, y=y, w=imgw, h=h)
            x += imgw + wm
            txt = str(i) + ' - ' + attendee.name
            texth = (h - th)/2
            self._pdf.text(x=x,
                           y=y+h-texth, txt=txt)
            x += maxname + wm
            self._pdf.line(x1=x, y1=y+h,
                           x2=x+signaturew, y2=y+h)
            x += signaturew + wm
            self._pdf.rect(x=x, y=y, w=oiqw, h=h)
            y += h + hm

            self._pdf.set_y(y)
            if self._pdf.y >= self._pdf.h:
                self._pdf.add_page()
                di = 0
                offy = 5
                y = self._pdf.y
            i += 1
            di += 1

    def _create_png_avatar(self, path):
        name = os.path.basename(path).split('.')[0]
        data_path = os.path.join(self._data_path, 'img/users/pdf/')
        os.makedirs(data_path, exist_ok=True)
        pdf_path = data_path + name + '.png'
        if not os.path.exists(pdf_path):
            img = Image.open(path)
            img.save(pdf_path)
        return pdf_path

    def _calculate_max_namesize(self):
        self._pdf.set_font("Arial", '', size=12)
        maxname = 0
        i = 0
        for attendee in self._event.attendees:
            txt = str(i) + ' - ' + attendee.name
            w = self._pdf.get_string_width(txt)
            if w > maxname:
                maxname = w
            i += 1
        return maxname

    def _print_attendees_head(self, imgw, maxname, signaturew, oiqw, wm):
        self._pdf.set_font("Arial", 'B', size=15)
        self._pdf.set_line_width(1)
        self._pdf.cell(imgw+wm, self._pdf.font_size*1.5, border=0)
        self._pdf.cell(maxname+wm, self._pdf.font_size*1.5, txt='Name', ln=0,
                       border=1,  align="L")
        self._pdf.cell(signaturew+wm, self._pdf.font_size*1.5, txt='Signature',
                       border=1, align="L")
        self._pdf.cell(oiqw+wm, self._pdf.font_size*1.5, txt='OIQ',
                       border=1, align="L")
        self._pdf.ln(self._pdf.font_size*2)
