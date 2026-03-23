import smtplib
from email.message import EmailMessage


def envoie_mail(mail_user,login,mdp):
    

    email = EmailMessage()

#les en-têtes de l'email
    email['From'] = ''
    email['To'] = mail_user
    email['Subject'] = 'C est un test pour envoyer les login et mdp'

    email.set_content("Bonjour voici votre identifiant : " +login+ " et votre mot de passe : "+mdp)

# Informations du serveur SMTP
    smtp_server = 'smtp.gmail.com'
    port = 587  # Port recommandé pour le chiffrement TLS
    username = ''
    password = ''

# # Connexion au serveur
    try:
        with smtplib.SMTP(smtp_server, port) as server:
            server.starttls()
            server.login(username, password)
            server.send_message(email)
            print("Les identifiants ont été envoyé par mail")
    except smtplib.SMTPConnectError:
         print("Erreur de connexion au serveur SMTP.")
    except smtplib.SMTPAuthenticationError:
         print("Erreur d'authentification. Veuillez vérifier vos identifiants.")
    except Exception as e:
        print(f"Une erreur s'est produite : {e}")
        