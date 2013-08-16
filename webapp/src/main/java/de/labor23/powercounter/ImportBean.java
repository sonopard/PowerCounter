package de.labor23.powercounter;

import java.util.Calendar;
import java.util.Date;

import javax.annotation.PostConstruct;

import org.primefaces.model.chart.LineChartSeries;
import org.springframework.stereotype.Component;
import org.springframework.transaction.annotation.Transactional;

import de.labor23.powercounter.dm.PowerMeter;
import de.labor23.powercounter.dm.Tick;
import de.labor23.powercounter.dm.User;
import de.labor23.powercounter.dm.hardware.Bank;

@Component
@Transactional
public class ImportBean {

	@PostConstruct
	public void setUp() throws Exception {
		
		User u = new User();
		u.setUsername("user");
		u.setPassword("user");
		u.setEnabled(true);
		u.persist();
		
		PowerMeter p = new PowerMeter();
		p.setAddress((byte) 23);
		p.setBank(Bank.LOWER_BANK);
		p.setMeterName("AV labordomäne");
		p.persist();
		
		u.getPowerMeters().add(p);
		u.merge();	
		

		Tick t;
        Date now = new Date();
        Date tickdate;

    	Integer timeDelta = 6000;
    	Integer datapoints = 6000;
    	
        for(int i = 0; i<datapoints; i++) {
        	
        	t = new Tick();
        	tickdate = new Date(now.getTime()-(i*i));
        	t.setOccurence(tickdate);
        	t.setMeter(p);
        	t.persist();
        }
	}
}
