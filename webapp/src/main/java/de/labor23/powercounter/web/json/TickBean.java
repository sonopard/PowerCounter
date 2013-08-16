package de.labor23.powercounter.web.json;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.util.Calendar;

import javax.annotation.PostConstruct;
import javax.faces.application.FacesMessage;
import javax.faces.bean.ApplicationScoped;
import javax.faces.bean.ManagedBean;
import javax.faces.context.FacesContext;

import org.apache.log4j.Level;
import org.apache.log4j.Logger;
import org.primefaces.json.JSONObject;
import org.springframework.http.HttpEntity;

import sun.net.www.http.HttpClient;

@ManagedBean
@ApplicationScoped
public class TickBean {

	public void getJson() {
		
	}
	
    @PostConstruct
    public void kurlariYukle() {
 
        HttpClient webIstemci = new DefaultHttpClient();
        HttpGet webdenGetir = new HttpGet(ERURL);
        HttpResponse donenCevap;
 
        try {
            donenCevap = webIstemci.execute(webdenGetir); // Getting the web (HTML) response from the URL
            HttpEntity birim = donenCevap.getEntity(); // Setting the HttpEntity to the Http Response object
            if (birim != null) {
                InputStream gelenVeri = birim.getContent();
                String sonuc = convertStreamToString(gelenVeri);
 
                JSONObject json = new JSONObject(sonuc);
                JSONObject currs = json.getJSONObject("rates");
 
                msj = APPINFO.concat(json.getString("license" ));
 
                erate.setBaseCurrency(json.getString("base" ));
                erate.setEur         (currs.getDouble("EUR"));  // Euro
                erate.setGbp         (currs.getDouble("GBP"));  // British Pound Sterling
                erate.setJpy         (currs.getDouble("JPY"));  // Japanese Yen
                erate.setCad         (currs.getDouble("CAD"));  // Canadian Dollars
                erate.setMxn         (currs.getDouble("MXN"));  // Mexican Pezo
                erate.setAed         (currs.getDouble("AED"));  // United Arab Emirates Dirham
                erate.setTrl         (currs.getDouble("TRY"));  // Turkish Lira
 
                long t = json.getLong("timestamp"); // getting the last update date &amp; time
 
                Calendar cal = Calendar.getInstance();
                cal.setTimeInMillis(t*1000); // converting into a human-readable date format
 
                erate.setLastModif(cal.getTime());
 
                erate.setDisclaimer(json.getString("disclaimer").concat(APPINFO.replaceAll("\\", ""))); // Getting the disclaimer and stripping the HTML tags from the APPINFO String before concatenating it
                erate.setMesaj         (msj);
 
                FacesMessage facesMsg = new FacesMessage(FacesMessage.SEVERITY_INFO, msj, msj);
                FacesContext.getCurrentInstance().addMessage("successInfo", facesMsg);
 
                gelenVeri.close();
            }
        } catch (Exception e) {
            msj= "Loading the exchange rates failed!\nThere appears to be a problem with the server connection.";
            erate.setMesaj(msj);
            Logger.getLogger(ExchangeRatesBean.class.getName()).log(Level.ERROR, null, e);
            FacesMessage facesMsg = new FacesMessage(FacesMessage.SEVERITY_ERROR, msj, msj);
            FacesContext.getCurrentInstance().addMessage(null, facesMsg);
        }
 
    }
 
    public String convertStreamToString(InputStream is) {
        // The incoming input stream is accumulated in a String to be returned
        BufferedReader reader = new BufferedReader(new InputStreamReader(is));
        StringBuilder sb = new StringBuilder();
        String line = null;
        try {
            while ((line = reader.readLine()) != null) {
                sb.append(line).append("\n");
            }
        } catch (IOException e) {
        } finally {
            try {
                is.close();
            } catch (IOException e) {
            }
        }
        return sb.toString();
    }
}
