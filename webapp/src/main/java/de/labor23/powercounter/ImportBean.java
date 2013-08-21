package de.labor23.powercounter;

import java.util.Date;

import javax.annotation.PostConstruct;

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
		p.setPin(7);
		p.setUser(u);
		p.persist();

		//System.out.println(u.getPowerMeters());
		/*
		Tick t;
		Date now = new Date();
		Date tickdate;

		Integer timeDelta = 6000;
		Integer datapoints = 6000;

		for (int i = 0; i < datapoints; i++) {

			t = new Tick();
			tickdate = new Date(now.getTime() - ((i * i) - 30000));
			t.setOccurence(tickdate);
			t.setMeter(p);
			t.persist();
		}
		*/
		/**
		 * Create a unused PowerMeter
		 */
		for (int i = 0; i < 5; i++) {
			p = new PowerMeter();
			p.setAddress((byte) (42+i));
			p.setBank(Bank.UPPER_BANK);
			p.setPin(7);
			p.setMeterName("Some unused meter "+i);
			p.persist();
		}
		
		/**
		 * Create unused User
		 */
		
		u = new User();
		u.setUsername("unUUsed");
		u.setPassword("unUUsed");
		u.setEnabled(true);
		u.persist();
	}
}
