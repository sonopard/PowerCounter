package de.labor23.powercounter.dm.json;
import org.springframework.roo.addon.javabean.RooJavaBean;
import org.springframework.roo.addon.jpa.activerecord.RooJpaActiveRecord;
import org.springframework.roo.addon.jpa.entity.RooJpaEntity;
import org.springframework.roo.addon.tostring.RooToString;

import java.util.Date;

import javax.persistence.Temporal;
import javax.persistence.TemporalType;
import javax.validation.constraints.NotNull;

import org.springframework.format.annotation.DateTimeFormat;

import javax.persistence.ManyToOne;

import org.springframework.roo.addon.json.RooJson;

import de.labor23.powercounter.dm.hardware.Bank;

import javax.persistence.Enumerated;
import javax.validation.constraints.Max;
import javax.validation.constraints.Min;

@RooJavaBean
@RooToString
@RooJson
public class TickDTO {

    @Temporal(TemporalType.TIMESTAMP)
    private Date occurence = new Date();

    @NotNull
    private Byte address;

    @NotNull
    @Min(0L)
    @Max(1L)
    private Integer bank;
    
    @NotNull
    @Min(0L)
    @Max(7L)
    private Integer pin;
}
