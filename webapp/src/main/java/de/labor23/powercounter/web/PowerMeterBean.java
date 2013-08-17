package de.labor23.powercounter.web;
import java.util.List;

import javax.annotation.PostConstruct;
import javax.faces.bean.ManagedBean;
import javax.faces.bean.ViewScoped;

import org.springframework.roo.addon.configurable.RooConfigurable;
import org.springframework.roo.addon.javabean.RooJavaBean;
import org.springframework.roo.addon.serializable.RooSerializable;

import de.labor23.powercounter.dm.PowerMeter;

@RooSerializable
@RooJavaBean
@RooConfigurable
@ManagedBean
@ViewScoped
public class PowerMeterBean {
	private PowerMeter powerMeter;
	
	private List<PowerMeter> allPowerMeters;
	private List<PowerMeter> unusedPowerMeters;
	
	
	
	@PostConstruct
	private void setUp() {
		allPowerMeters = PowerMeter.findAllPowerMeters();
		unusedPowerMeters = PowerMeter.findPowerMetersByUserIsNull().getResultList();
	}
	
	/**
	 * Free a powerMeter from its user
	 */
	public void free() {
		free(powerMeter);
	}
	public void free(PowerMeter p) {
		p.setUser(null);
		p = p.merge();
		unusedPowerMeters.add(p);
	}
	
	
	/**
	 * Creation of PowerMeter
	 */

	public void create() {
		powerMeter = new PowerMeter();
	}
	public void persist() {
		powerMeter.persist();
		unusedPowerMeters.add(powerMeter);
		allPowerMeters.add(powerMeter);
		//setUp();
	}
}
