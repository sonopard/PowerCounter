package de.labor23.powercounter.dm;
import javax.persistence.EntityManager;
import javax.persistence.Enumerated;
import javax.persistence.ManyToOne;
import javax.persistence.Table;
import javax.persistence.TypedQuery;
import javax.persistence.UniqueConstraint;
import javax.validation.constraints.NotNull;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.roo.addon.javabean.RooJavaBean;
import org.springframework.roo.addon.jpa.activerecord.RooJpaActiveRecord;
import org.springframework.roo.addon.tostring.RooToString;

import de.labor23.powercounter.dm.hardware.Bank;

@RooJavaBean
@RooToString
@RooJpaActiveRecord(entityName = "PowerMeter", finders = { "findPowerMetersByGpioIdEquals", "findPowerMetersByAddress" })
@Table(uniqueConstraints=@UniqueConstraint(columnNames = { "ADDRESS", "BANK" }))
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
    
    
    @NotNull
    @ManyToOne
    private User user;
    
    public static PowerMeter findPowerMetersByAddressAndBank(Byte address, Bank bank) {
        if (address == null) throw new IllegalArgumentException("The address argument is required");
        if (bank == null) throw new IllegalArgumentException("The bank argument is required");
        EntityManager em = PowerMeter.entityManager();
        TypedQuery<PowerMeter> q = em.createQuery(""
        		+ "SELECT o FROM PowerMeter AS o "
        		+ "WHERE "
        			+ "o.address = :address "
        		+ "AND "
        			+ "o.bank = :bank ", PowerMeter.class);
        q.setParameter("address", address);
        q.setParameter("bank", bank);
        return q.getSingleResult();
    }
}
