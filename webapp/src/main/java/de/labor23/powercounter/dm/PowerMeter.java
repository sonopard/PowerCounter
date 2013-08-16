package de.labor23.powercounter.dm;
import org.springframework.roo.addon.javabean.RooJavaBean;
import org.springframework.roo.addon.jpa.activerecord.RooJpaActiveRecord;
import org.springframework.roo.addon.tostring.RooToString;

import javax.persistence.Column;
import javax.persistence.EntityManager;
import javax.persistence.Enumerated;
import javax.persistence.TypedQuery;
import javax.validation.constraints.Min;
import javax.validation.constraints.NotNull;

import org.springframework.beans.factory.annotation.Value;

import de.labor23.powercounter.dm.hardware.Bank;

@RooJavaBean
@RooToString
@RooJpaActiveRecord(entityName = "PowerMeter", finders = { "findPowerMetersByGpioIdEquals", "findPowerMetersByAddress" })
public class PowerMeter {

    /**
     */
    private String meterName;

    /**
     */
    @NotNull
    private Byte address;
    
    /**
     */
    @NotNull
    @Enumerated
    private Bank bank;

    /**
     */
    @NotNull
    @Value("2000")
    private Integer ticksPerKWH;
    
    
    public static TypedQuery<PowerMeter> findPowerMetersByAddressAndBank(Byte address, Bank bank) {
        if (address == null) throw new IllegalArgumentException("The address argument is required");
        if (bank == null) throw new IllegalArgumentException("The bank argument is required");
        EntityManager em = PowerMeter.entityManager();
        TypedQuery<PowerMeter> q = em.createQuery(""
        		+ "SELECT o FROM PowerMeter AS o "
        		+ "WHERE "
        			+ "o.address = :address"
        		+ "AND"
        			+ "o.bank = :bank", PowerMeter.class);
        q.setParameter("address", address);
        q.setParameter("address", bank);
        return q;
    }
}
