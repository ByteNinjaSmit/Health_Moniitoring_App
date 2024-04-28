from types import GeneratorType
import smtplib

from notification import errors


class NotificationService(object):

    swallowSMTPErrors = False
    emailFromAddress = None


    def __init__(self, smtpHost, emailFromAddress=None, swallowSMTPErrors=None):
        self.smtpHost = smtpHost
        if emailFromAddress is not None:
            self.emailFromAddress = emailFromAddress
        if swallowSMTPErrors is not None:
            self.swallowSMTPErrors = swallowSMTPErrors


    def sendEmail(self, toAddresses, msg, fromAddress=None, swallowErrors=None):
        """
        Send an email to one or more recipients.
        """

        # If toAddresses is not already a list type then make it so.
        if not isinstance(toAddresses, (list, tuple, GeneratorType)):
            toAddresses = [toAddresses]

        # Work out whether to swallow errors.
        if swallowErrors is None:
            swallowErrors = self.swallowSMTPErrors

        # Work out the from address to use.
        if fromAddress is None:
            fromAddress = self.emailFromAddress

        # Send the email
        try:
            server = smtplib.SMTP(self.smtpHost)
            r = server.sendmail(fromAddress, toAddresses, str(msg))
        except smtplib.SMTPException, e:
            # Swallow smtp errors if requested
            if not swallowErrors:
                raise errors.MailNotificationError(str(e.value))

        return r


    def buildEmailFromTemplate(self, templateName, templateArgs, headers):
        raise NotImplementedError("buildEmailFromTemplate must be "\
                "implemented by a subclass")

