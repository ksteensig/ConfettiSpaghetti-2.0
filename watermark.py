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

    def __call__(self, image):
        self.font.push()
        size = max(image.width, image.height)

        result = image.clone()
        sendertext = " Sender: {0} \n Sender-mail: {1} ".format(*self.internal)
        receivertext = " Recipient: {2} \n Recipient-mail: {3} ".format(*self.internal)
        #wraptext = wrap(text, 20)
        fontsize = size//40
        self.font.font_size = fontsize
        textheight = 3*image.height//5
        sendwidth = int(self.font.get_font_metrics(image, sendertext, True).text_width)

        self.font.text(fontsize, textheight, sendertext)
        self.font.text(fontsize + sendwidth, textheight, receivertext)
        self.font.draw(result)

        with self.stud.clone() as newstud:
            if size < 4000:
                newstud.resize(size, size)
            result.composite(newstud, 0, textheight - (newstud.height + fontsize))
            result.composite(newstud, 0, textheight + fontsize)

        self.font.pop()
        return result


with Image(filename='Klodsmajor.JPG') as img:
    marking = Watermark("Me", "gmail", "You", "hotmail")
    result = marking(img)
    result.save(filename='Edit.png')
    display(result)
