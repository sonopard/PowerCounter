package de.labor23.powercounter.dm;
import javax.persistence.EntityManager;
import javax.persistence.Enumerated;
import javax.persistence.ManyToOne;
import javax.persistence.Table;
import javax.persistence.TypedQuery;
import javax.persistence.UniqueConstraint;
import javax.validation.constraints.Max;
import javax.validation.constraints.Min;
import javax.validation.constraints.NotNull;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.roo.addon.javabean.RooJavaBean;
import org.springframework.roo.addon.jpa.activerecord.RooJpaActiveRecord;
import org.springframework.roo.addon.tostring.RooToString;

import de.labor23.powercounter.dm.hardware.Bank;

@RooJavaBean
@RooToString
@Table(uniqueConstraints = @UniqueConstraint(columnNames = { "ADDRESS", "BANK", "PIN" }))
@RooJpaActiveRecord(entityName = "PowerMeter", finders = { "findPowerMetersByAddress", "findPowerMetersByUserIsNull", "findPowerMetersByUser" })
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
    
    @NotNull
    @Min(0L)
    @Max(7L)
    private Integer pin;
    
    /**
     */
    @NotNull
    @Value("2000")
    private Integer ticksPerKWH;

    @ManyToOne
    private User user;

    public static PowerMeter findPowerMetersByAddressAndBankAndPin(Byte address, Bank bank, Integer pin) {
        if (address == null) throw new IllegalArgumentException("The address argument is required");
        if (bank == null) throw new IllegalArgumentException("The bank argument is required");
        if (pin == null) throw new IllegalArgumentException("The pin argument is required");
        EntityManager em = PowerMeter.entityManager();
        TypedQuery<PowerMeter> q = em.createQuery("" + 
        "SELECT o FROM PowerMeter AS o " + 
        "WHERE " + 
        	"o.address = :address " + 
        "AND " + 
        	"o.bank = :bank " + 
        "AND "
        	+ "o.pin = :pin", PowerMeter.class);
        q.setParameter("address", address);
        q.setParameter("bank", bank);
        q.setParameter("pin", pin);
        return q.getSingleResult();
    }
}
