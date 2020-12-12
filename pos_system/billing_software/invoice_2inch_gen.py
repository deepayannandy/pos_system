from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4,A5
from reportlab.lib import pdfencrypt
from reportlab.lib.units import inch, mm



mid=80

def genpdf(company,items,total,mod):
    pagesize=(56*mm,500*mm)
    pdf= canvas.Canvas("media/bills/"+str(company[1])+'.pdf',bottomup=0,pagesize=pagesize)
    pdf.setLineWidth(.3)
    pdf.setFont("Helvetica", 10)
    pdf.drawCentredString(mid,10,"Invoice")
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawCentredString(mid, 25, company[0])
    pdf.setFont("Helvetica", 9)
    pdf.drawCentredString(mid, 35, company[3])
    pdf.drawCentredString(mid, 35, company[3])
    pdf.drawCentredString(mid, 45, str(company[4]))
    pdf.drawString(3,58,"Invoive No. "+str(company[1]))
    pdf.drawString(3,68,"Date:"+company[2])
    pdf.setFont("Helvetica", 12)
    pdf.drawString(0,74,"-"*60)
    pdf.setFont("Helvetica", 8)
    pdf.drawCentredString(mid, 80, "Sl    Product          qt      Price      Amt      ")
    pdf.setFont("Helvetica", 12)
    pdf.drawString(0, 88, "-" * 60)
    pdf.setFont("Helvetica", 9)
    j=0
    y=95
    for i in items:
        pdf.drawString(8,y,str(j+1))
        pdf.drawString(20,y,i[0][:10])
        pdf.drawString(75, y, str(i[2]))
        pdf.drawString(90, y, str(i[1]))
        pdf.drawString(122, y, str(int(i[2])*int(i[1])))
        j+=1
        y += 10
    pdf.setFont("Helvetica", 12)
    pdf.drawString(0, y, "-" * 60)
    pdf.setFont("Helvetica", 9)
    pdf.drawString(10,y+10,"Subtotal:")
    pdf.drawString(90, y + 10, "Rs."+str(total))
    pdf.drawString(10, y + 20, "GST "+str(company[5])+"%:")
    pdf.drawString(90, y + 20, "Rs." + str((total/100)*company[5]))
    pdf.setFont("Helvetica-Bold", 10)
    pdf.drawString(10, y + 30, "TOTAL:")
    pdf.drawString(90, y + 30, "Rs." + str(total+(total / 100) * company[5]))
    pdf.setFont("Helvetica-Bold", 8)
    pdf.drawString(10, y + 40, "Mode of Payment:")
    pdf.drawString(90, y + 40, mod.split()[0])
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawCentredString(mid, y + 80, "Thank You Visit Again!")
    pdf.save()
    return "media/bills/"+str(company[1])+'.pdf'

