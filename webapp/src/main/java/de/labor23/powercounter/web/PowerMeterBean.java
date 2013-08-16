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
	
	@PostConstruct
	private void setUp() {
		allPowerMeters = PowerMeter.findAllPowerMeters();
	}
	
}
