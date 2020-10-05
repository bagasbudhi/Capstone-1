from firebase import firebase



firebase = firebase.FirebaseApplication("https://micron-cd982.firebaseio.com/",None)

data = {
    'Name':'Bagas',
    'email':'budhi.mail',
    'no.':8094809492


}

result = firebase.post('/micron-cd982/',data)

print(result)