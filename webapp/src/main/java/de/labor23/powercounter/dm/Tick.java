package de.labor23.powercounter.dm;
import java.util.Date;

import javax.persistence.ManyToOne;
import javax.persistence.Temporal;
import javax.persistence.TemporalType;
import javax.validation.constraints.NotNull;

import org.springframework.format.annotation.DateTimeFormat;
import org.springframework.roo.addon.javabean.RooJavaBean;
import org.springframework.roo.addon.jpa.activerecord.RooJpaActiveRecord;
import org.springframework.roo.addon.tostring.RooToString;

import de.labor23.powercounter.dm.hardware.Bank;
import de.labor23.powercounter.dm.json.TickDTO;

@RooJavaBean
@RooToString
@RooJpaActiveRecord
public class Tick {

    /**
     */
    @NotNull
    @Temporal(TemporalType.TIMESTAMP)
    @DateTimeFormat(style = "M-")
    private Date occurence;

    /**
     */
    @NotNull
    @ManyToOne
    private PowerMeter meter;
    
    public Tick(TickDTO dto) {
    	this.occurence = dto.getOccurence();
    	PowerMeter p =  PowerMeter.findPowerMetersByAddressAndBank(dto.getAddress(), Bank.values()[dto.getBank()]);
    	this.meter = p;
    }
}
