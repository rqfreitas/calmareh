from icalendar import Calendar, Event


f = open("myfile.ics", "x")

def registra_mareh(ano, nome_porto):
    f = open(ano+"_"+nome_porto+".ics", "w")
    f.write("BEGIN:VEVENT")
    f.write("DTSTART:"+ ano + mes + dia + "T"+ hora + minuto+"00")
    f.write("DTEND:20200326T235959")
    f.write("DTSTAMP:"+ ano + "0101T000000")

    f.write("ORGANIZER;CN=calmareh@rqf.fr:mailto:rodrigo@rqf.fr")
    
    f.write("DTSTAMP:"+ ano + "0101T000000")

    f.write("DESCRIPTION:  Calendário de marés do porto: "+ nome_porto +" no ano de "+ano+". Fonte: CPTEC/INPE-::~:~::~:~:~:~:~:~:~:~:~:~:~:~:~:~:~:~:~:~:~:~:~:~:~:~:~:~:~:~")

    f.write("DTSTAMP:"+ ano + "0101T000000")
    f.write("LOCATION:")
    f.write("SEQUENCE:0")
    f.write("STATUS:CONFIRMED")
    
    f.write("TRANSP:OPAQUE")
    f.write("END:VEVENT")



BEGIN:VEVENT
DTSTART:20200406T120000Z
DTEND:20200406T130000Z
DTSTAMP:20211210T025926Z
UID:cooj6d1m6oqjeb9nckq6cb9k74s62b9p6th6cb9m70rm6or670r3ce9l64@google.com
CREATED:20200406T012834Z
DESCRIPTION:
LAST-MODIFIED:20200406T012834Z
LOCATION:
SEQUENCE:0
STATUS:CONFIRMED
SUMMARY:Capelania Porto Social
TRANSP:OPAQUE
END:VEVENT


def begincal(nome_porto, ano):
    f = open(ano+"_"+nome_porto+".ics", "x")
    f = open(ano+"_"+nome_porto+".ics", "w")
    f.write("BEGIN:VCALENDAR")
    f.write("PRODID:-//Google Inc//Google Calendar 70.9054//EN")
    f.write("VERSION:2.0")
    f.write("METHOD:PUBLISH")
    f.write("BEGIN:VCALENDAR")
    f.write("X-WR-CALNAME:Maré - " + nome_porto + " - " + ano)
    f.write("X-WR-TIMEZONE:America/Recife")
    f.write("X-WR-CALDESC:Agenda Pastoral Mosaico")
    f.write("BEGIN:VTIMEZONE")
    f.write("TZID:America/Recife")
    f.write("X-LIC-LOCATION:America/Recife")
    f.write("BEGIN:STANDARD")
    f.write("TZOFFSETFROM:-0300")
    f.write("TZOFFSETTO:-0300")
    f.write("TZNAME:-03")
    f.write("DTSTART:19700101T000000")
    f.write("END:STANDARD")
    f.write("END:VTIMEZONE")




