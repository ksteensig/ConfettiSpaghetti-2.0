from wand.image import Image
from wand.display import display
from wand.drawing import Drawing
from wand.color import Color
from textwrap import wrap

class Watermark:
    font = Drawing()
    font.font = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
    font.fill_color = Color("White")
    font.fill_opacity = 0.5

    stud = Image(filename="StudTile.png")

    def __init__(self, sender, smail, recipient, rmail):
        self.internal = (sender, smail, recipient, rmail)

    def __call__(self, image, model, negate=False):
        self.font.push()
        size = max(image.width, image.height)

        result = image.clone()
        sendertext = " Sender: {0} \n Recipient: {2} ".format(*self.internal)
        receivertext = " Sender-mail: {1} \n Recipient-mail: {3} ".format(*self.internal)
        #wraptext = wrap(text, 20)
        fontsize = size//40
        self.font.font_size = fontsize
        textheight = 3*image.height//5
        sendwidth = int(self.font.get_font_metrics(image, sendertext, True).text_width)
        receivewidth = int(self.font.get_font_metrics(image, receivertext, True).text_width)

        if negate:
            self.font.fill_color = Color("Black")
            self.font.fill_opacity = 0.5
        self.font.text(fontsize, textheight, sendertext)
        self.font.text(fontsize + sendwidth, textheight, receivertext)
        self.font.font_size = int(1.5*fontsize)
        self.font.text(fontsize, textheight + fontsize * 3, " Model: {0}".format(model))
        self.font.draw(result)

        with self.stud.clone() as newstud:
            if size < 4000:
                newstud.resize(size, size)
            if negate:
                newstud.negate()
            result.composite(newstud, 0, textheight - (newstud.height + fontsize))
            result.composite(newstud, 0, textheight + fontsize * 2)

        self.font.pop()
        return result

'''
with Image(filename='VestaShilling.JPG') as img:
    marking = Watermark("Thomas Frandsen", "thomas.frandsen@hotmail.com", "Kasper Steensig", "kasper.steensig@gmail.com")
    result = marking(img, "27803", True)
    result.save(filename='Edit.png')
    display(result)
'''