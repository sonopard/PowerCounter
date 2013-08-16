package de.labor23.powercounter.dm;
import java.util.Date;

import javax.persistence.EntityManager;
import javax.persistence.ManyToOne;
import javax.persistence.Temporal;
import javax.persistence.TemporalType;
import javax.persistence.TypedQuery;
import javax.validation.constraints.NotNull;

import org.springframework.format.annotation.DateTimeFormat;
import org.springframework.roo.addon.javabean.RooJavaBean;
import org.springframework.roo.addon.jpa.activerecord.RooJpaActiveRecord;
import org.springframework.roo.addon.tostring.RooToString;

import de.labor23.powercounter.dm.hardware.Bank;
import de.labor23.powercounter.dm.json.TickDTO;

import java.util.Calendar;

@RooJavaBean
@RooToString
@RooJpaActiveRecord(finders = { "findTicksByMeter", "findTicksByOccurenceBetween" })
public class Tick {

    /**
     */
    @NotNull
    @Temporal(TemporalType.TIMESTAMP)
    @DateTimeFormat(pattern = "dd.MM.yyyy hh:mm:ss")
    private Date occurence;

    /**
     */
    @NotNull
    @ManyToOne
    private PowerMeter meter;

    public Tick(TickDTO dto) {
        this.occurence = dto.getOccurence();
        PowerMeter p = PowerMeter.findPowerMetersByAddressAndBank(dto.getAddress(), Bank.values()[dto.getBank()]);
        this.meter = p;
    }

    public static long countTicksByOccurenceBetweenAndMeter(Date minOccurence, Date maxOccurence, PowerMeter meter) {
        if (meter == null) throw new IllegalArgumentException("The meter argument is required");
        if (minOccurence == null) throw new IllegalArgumentException("The minOccurence argument is required");
        if (maxOccurence == null) throw new IllegalArgumentException("The maxOccurence argument is required");
        TypedQuery<Long> q = entityManager().createQuery("" + "SELECT COUNT(o) FROM Tick o " + "WHERE " + "o.meter = :meter " + "AND " + "(o.occurence BETWEEN :minOccurence AND :maxOccurence)", Long.class);
        q.setParameter("meter", meter);
        q.setParameter("minOccurence", minOccurence);
        q.setParameter("maxOccurence", maxOccurence);
        return q.getSingleResult();
    }
    
    
    
    public static long countTicksByOccurenceBetween(Date minOccurence, Date maxOccurence) {
        if (minOccurence == null) throw new IllegalArgumentException("The minOccurence argument is required");
        if (maxOccurence == null) throw new IllegalArgumentException("The maxOccurence argument is required");
        EntityManager em = Tick.entityManager();
        TypedQuery<Long> q = em.createQuery("SELECT COUNT(o) FROM Tick AS o WHERE o.occurence BETWEEN :minOccurence AND :maxOccurence", Long.class);
        q.setParameter("minOccurence", minOccurence);
        q.setParameter("maxOccurence", maxOccurence);
        return q.getSingleResult();
    }
}
