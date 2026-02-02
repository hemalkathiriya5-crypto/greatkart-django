import ssl
from django.core.mail.backends.smtp import EmailBackend as SMTPBackend


class SSLEmailBackend(SMTPBackend):
    """
    Custom email backend that disables SSL certificate verification.
    This is useful for development environments where SSL certificates
    may not be properly configured.
    """
    
    def open(self):
        """
        Override the open method to set ssl_context for STARTTLS connections.
        """
        if self.connection:
            return False
        
        connection_params = {
            'timeout': self.timeout,
        }
        
        if self.use_ssl:
            connection_params['context'] = ssl._create_unverified_context()
        
        try:
            self.connection = self.connection_class(
                self.host, self.port, **connection_params
            )
            
            # Set debuglevel if needed (0 = no debug, 1 = debug)
            self.connection.set_debuglevel(0)
            
            if self.use_tls:
                self.connection.ehlo()
                # Create unverified context for STARTTLS
                context = ssl._create_unverified_context()
                self.connection.starttls(context=context)
                self.connection.ehlo()
            
            if self.username and self.password:
                self.connection.login(self.username, self.password)
            
            return True
        except Exception:
            if not self.fail_silently:
                raise
