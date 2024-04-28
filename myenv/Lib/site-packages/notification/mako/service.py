from email.MIMEText import MIMEText
import os.path
from notification import service, emailbuilder
from mako.lookup import TemplateLookup
from mako.template import Template


class NotificationService(service.NotificationService):

    def __init__(self, *a, **k):
        emailTemplateDir = k.pop("emailTemplateDir")
        super(NotificationService, self).__init__(*a, **k)
        self.emailTemplateDir = emailTemplateDir
        self.lookup = TemplateLookup(directories=[emailTemplateDir])

    def buildEmailFromTemplate(self, templateName, templateArgs, headers):
        templateDir = os.path.join(self.emailTemplateDir, templateName)
        source = emailbuilder.FileSystemSource(templateDir)
        builder = TemplatedEmailBuilder(source, headers,
                                        templateArgs=templateArgs,
                                        lookup=self.lookup)
        return builder.build()



class TemplatedEmailBuilder(emailbuilder.EmailBuilder):

    def __init__(self, *a, **k):
        templateArgs = k.pop('templateArgs')
        lookup = k.pop('lookup')
        super(TemplatedEmailBuilder, self).__init__(*a, **k)
        self.templateArgs = templateArgs
        self.lookup = lookup

    def part_text(self, contentType, filename):
        template = self.source[filename].read()
        stream = Template(template, lookup=self.lookup)
        text = stream.render_unicode(**self.templateArgs)
        return MIMEText(text.encode('utf-8'), contentType[1], 'utf-8')

