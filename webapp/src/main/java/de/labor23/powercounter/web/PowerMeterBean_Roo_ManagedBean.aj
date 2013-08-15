// WARNING: DO NOT EDIT THIS FILE. THIS FILE IS MANAGED BY SPRING ROO.
// You may push code into the target .java compilation unit if you wish to edit any member(s).

package de.labor23.powercounter.web;

import de.labor23.powercounter.dm.PowerMeter;
import de.labor23.powercounter.web.PowerMeterBean;
import de.labor23.powercounter.web.util.MessageFactory;
import java.util.ArrayList;
import java.util.List;
import javax.annotation.PostConstruct;
import javax.el.ELContext;
import javax.el.ExpressionFactory;
import javax.faces.application.FacesMessage;
import javax.faces.bean.ManagedBean;
import javax.faces.bean.SessionScoped;
import javax.faces.component.html.HtmlOutputText;
import javax.faces.component.html.HtmlPanelGrid;
import javax.faces.context.FacesContext;
import javax.faces.validator.LongRangeValidator;
import org.primefaces.component.inputtext.InputText;
import org.primefaces.component.message.Message;
import org.primefaces.component.outputlabel.OutputLabel;
import org.primefaces.component.spinner.Spinner;
import org.primefaces.context.RequestContext;
import org.primefaces.event.CloseEvent;

privileged aspect PowerMeterBean_Roo_ManagedBean {
    
    declare @type: PowerMeterBean: @ManagedBean(name = "powerMeterBean");
    
    declare @type: PowerMeterBean: @SessionScoped;
    
    private String PowerMeterBean.name = "PowerMeters";
    
    private PowerMeter PowerMeterBean.powerMeter;
    
    private List<PowerMeter> PowerMeterBean.allPowerMeters;
    
    private boolean PowerMeterBean.dataVisible = false;
    
    private List<String> PowerMeterBean.columns;
    
    private HtmlPanelGrid PowerMeterBean.createPanelGrid;
    
    private HtmlPanelGrid PowerMeterBean.editPanelGrid;
    
    private HtmlPanelGrid PowerMeterBean.viewPanelGrid;
    
    private boolean PowerMeterBean.createDialogVisible = false;
    
    @PostConstruct
    public void PowerMeterBean.init() {
        columns = new ArrayList<String>();
        columns.add("gpioId");
        columns.add("meterName");
    }
    
    public String PowerMeterBean.getName() {
        return name;
    }
    
    public List<String> PowerMeterBean.getColumns() {
        return columns;
    }
    
    public List<PowerMeter> PowerMeterBean.getAllPowerMeters() {
        return allPowerMeters;
    }
    
    public void PowerMeterBean.setAllPowerMeters(List<PowerMeter> allPowerMeters) {
        this.allPowerMeters = allPowerMeters;
    }
    
    public String PowerMeterBean.findAllPowerMeters() {
        allPowerMeters = PowerMeter.findAllPowerMeters();
        dataVisible = !allPowerMeters.isEmpty();
        return null;
    }
    
    public boolean PowerMeterBean.isDataVisible() {
        return dataVisible;
    }
    
    public void PowerMeterBean.setDataVisible(boolean dataVisible) {
        this.dataVisible = dataVisible;
    }
    
    public HtmlPanelGrid PowerMeterBean.getCreatePanelGrid() {
        if (createPanelGrid == null) {
            createPanelGrid = populateCreatePanel();
        }
        return createPanelGrid;
    }
    
    public void PowerMeterBean.setCreatePanelGrid(HtmlPanelGrid createPanelGrid) {
        this.createPanelGrid = createPanelGrid;
    }
    
    public HtmlPanelGrid PowerMeterBean.getEditPanelGrid() {
        if (editPanelGrid == null) {
            editPanelGrid = populateEditPanel();
        }
        return editPanelGrid;
    }
    
    public void PowerMeterBean.setEditPanelGrid(HtmlPanelGrid editPanelGrid) {
        this.editPanelGrid = editPanelGrid;
    }
    
    public HtmlPanelGrid PowerMeterBean.getViewPanelGrid() {
        return populateViewPanel();
    }
    
    public void PowerMeterBean.setViewPanelGrid(HtmlPanelGrid viewPanelGrid) {
        this.viewPanelGrid = viewPanelGrid;
    }
    
    public HtmlPanelGrid PowerMeterBean.populateCreatePanel() {
        FacesContext facesContext = FacesContext.getCurrentInstance();
        javax.faces.application.Application application = facesContext.getApplication();
        ExpressionFactory expressionFactory = application.getExpressionFactory();
        ELContext elContext = facesContext.getELContext();
        
        HtmlPanelGrid htmlPanelGrid = (HtmlPanelGrid) application.createComponent(HtmlPanelGrid.COMPONENT_TYPE);
        
        OutputLabel gpioIdCreateOutput = (OutputLabel) application.createComponent(OutputLabel.COMPONENT_TYPE);
        gpioIdCreateOutput.setFor("gpioIdCreateInput");
        gpioIdCreateOutput.setId("gpioIdCreateOutput");
        gpioIdCreateOutput.setValue("Gpio Id:");
        htmlPanelGrid.getChildren().add(gpioIdCreateOutput);
        
        Spinner gpioIdCreateInput = (Spinner) application.createComponent(Spinner.COMPONENT_TYPE);
        gpioIdCreateInput.setId("gpioIdCreateInput");
        gpioIdCreateInput.setValueExpression("value", expressionFactory.createValueExpression(elContext, "#{powerMeterBean.powerMeter.gpioId}", Integer.class));
        gpioIdCreateInput.setRequired(true);
        gpioIdCreateInput.setMin(1.0);
        LongRangeValidator gpioIdCreateInputValidator = new LongRangeValidator();
        gpioIdCreateInputValidator.setMinimum(1);
        gpioIdCreateInput.addValidator(gpioIdCreateInputValidator);
        
        htmlPanelGrid.getChildren().add(gpioIdCreateInput);
        
        Message gpioIdCreateInputMessage = (Message) application.createComponent(Message.COMPONENT_TYPE);
        gpioIdCreateInputMessage.setId("gpioIdCreateInputMessage");
        gpioIdCreateInputMessage.setFor("gpioIdCreateInput");
        gpioIdCreateInputMessage.setDisplay("icon");
        htmlPanelGrid.getChildren().add(gpioIdCreateInputMessage);
        
        OutputLabel meterNameCreateOutput = (OutputLabel) application.createComponent(OutputLabel.COMPONENT_TYPE);
        meterNameCreateOutput.setFor("meterNameCreateInput");
        meterNameCreateOutput.setId("meterNameCreateOutput");
        meterNameCreateOutput.setValue("Meter Name:");
        htmlPanelGrid.getChildren().add(meterNameCreateOutput);
        
        InputText meterNameCreateInput = (InputText) application.createComponent(InputText.COMPONENT_TYPE);
        meterNameCreateInput.setId("meterNameCreateInput");
        meterNameCreateInput.setValueExpression("value", expressionFactory.createValueExpression(elContext, "#{powerMeterBean.powerMeter.meterName}", String.class));
        meterNameCreateInput.setRequired(false);
        htmlPanelGrid.getChildren().add(meterNameCreateInput);
        
        Message meterNameCreateInputMessage = (Message) application.createComponent(Message.COMPONENT_TYPE);
        meterNameCreateInputMessage.setId("meterNameCreateInputMessage");
        meterNameCreateInputMessage.setFor("meterNameCreateInput");
        meterNameCreateInputMessage.setDisplay("icon");
        htmlPanelGrid.getChildren().add(meterNameCreateInputMessage);
        
        return htmlPanelGrid;
    }
    
    public HtmlPanelGrid PowerMeterBean.populateEditPanel() {
        FacesContext facesContext = FacesContext.getCurrentInstance();
        javax.faces.application.Application application = facesContext.getApplication();
        ExpressionFactory expressionFactory = application.getExpressionFactory();
        ELContext elContext = facesContext.getELContext();
        
        HtmlPanelGrid htmlPanelGrid = (HtmlPanelGrid) application.createComponent(HtmlPanelGrid.COMPONENT_TYPE);
        
        OutputLabel gpioIdEditOutput = (OutputLabel) application.createComponent(OutputLabel.COMPONENT_TYPE);
        gpioIdEditOutput.setFor("gpioIdEditInput");
        gpioIdEditOutput.setId("gpioIdEditOutput");
        gpioIdEditOutput.setValue("Gpio Id:");
        htmlPanelGrid.getChildren().add(gpioIdEditOutput);
        
        Spinner gpioIdEditInput = (Spinner) application.createComponent(Spinner.COMPONENT_TYPE);
        gpioIdEditInput.setId("gpioIdEditInput");
        gpioIdEditInput.setValueExpression("value", expressionFactory.createValueExpression(elContext, "#{powerMeterBean.powerMeter.gpioId}", Integer.class));
        gpioIdEditInput.setRequired(true);
        gpioIdEditInput.setMin(1.0);
        LongRangeValidator gpioIdEditInputValidator = new LongRangeValidator();
        gpioIdEditInputValidator.setMinimum(1);
        gpioIdEditInput.addValidator(gpioIdEditInputValidator);
        
        htmlPanelGrid.getChildren().add(gpioIdEditInput);
        
        Message gpioIdEditInputMessage = (Message) application.createComponent(Message.COMPONENT_TYPE);
        gpioIdEditInputMessage.setId("gpioIdEditInputMessage");
        gpioIdEditInputMessage.setFor("gpioIdEditInput");
        gpioIdEditInputMessage.setDisplay("icon");
        htmlPanelGrid.getChildren().add(gpioIdEditInputMessage);
        
        OutputLabel meterNameEditOutput = (OutputLabel) application.createComponent(OutputLabel.COMPONENT_TYPE);
        meterNameEditOutput.setFor("meterNameEditInput");
        meterNameEditOutput.setId("meterNameEditOutput");
        meterNameEditOutput.setValue("Meter Name:");
        htmlPanelGrid.getChildren().add(meterNameEditOutput);
        
        InputText meterNameEditInput = (InputText) application.createComponent(InputText.COMPONENT_TYPE);
        meterNameEditInput.setId("meterNameEditInput");
        meterNameEditInput.setValueExpression("value", expressionFactory.createValueExpression(elContext, "#{powerMeterBean.powerMeter.meterName}", String.class));
        meterNameEditInput.setRequired(false);
        htmlPanelGrid.getChildren().add(meterNameEditInput);
        
        Message meterNameEditInputMessage = (Message) application.createComponent(Message.COMPONENT_TYPE);
        meterNameEditInputMessage.setId("meterNameEditInputMessage");
        meterNameEditInputMessage.setFor("meterNameEditInput");
        meterNameEditInputMessage.setDisplay("icon");
        htmlPanelGrid.getChildren().add(meterNameEditInputMessage);
        
        return htmlPanelGrid;
    }
    
    public HtmlPanelGrid PowerMeterBean.populateViewPanel() {
        FacesContext facesContext = FacesContext.getCurrentInstance();
        javax.faces.application.Application application = facesContext.getApplication();
        ExpressionFactory expressionFactory = application.getExpressionFactory();
        ELContext elContext = facesContext.getELContext();
        
        HtmlPanelGrid htmlPanelGrid = (HtmlPanelGrid) application.createComponent(HtmlPanelGrid.COMPONENT_TYPE);
        
        HtmlOutputText gpioIdLabel = (HtmlOutputText) application.createComponent(HtmlOutputText.COMPONENT_TYPE);
        gpioIdLabel.setId("gpioIdLabel");
        gpioIdLabel.setValue("Gpio Id:");
        htmlPanelGrid.getChildren().add(gpioIdLabel);
        
        HtmlOutputText gpioIdValue = (HtmlOutputText) application.createComponent(HtmlOutputText.COMPONENT_TYPE);
        gpioIdValue.setValueExpression("value", expressionFactory.createValueExpression(elContext, "#{powerMeterBean.powerMeter.gpioId}", String.class));
        htmlPanelGrid.getChildren().add(gpioIdValue);
        
        HtmlOutputText meterNameLabel = (HtmlOutputText) application.createComponent(HtmlOutputText.COMPONENT_TYPE);
        meterNameLabel.setId("meterNameLabel");
        meterNameLabel.setValue("Meter Name:");
        htmlPanelGrid.getChildren().add(meterNameLabel);
        
        HtmlOutputText meterNameValue = (HtmlOutputText) application.createComponent(HtmlOutputText.COMPONENT_TYPE);
        meterNameValue.setId("meterNameValue");
        meterNameValue.setValueExpression("value", expressionFactory.createValueExpression(elContext, "#{powerMeterBean.powerMeter.meterName}", String.class));
        htmlPanelGrid.getChildren().add(meterNameValue);
        
        return htmlPanelGrid;
    }
    
    public PowerMeter PowerMeterBean.getPowerMeter() {
        if (powerMeter == null) {
            powerMeter = new PowerMeter();
        }
        return powerMeter;
    }
    
    public void PowerMeterBean.setPowerMeter(PowerMeter powerMeter) {
        this.powerMeter = powerMeter;
    }
    
    public String PowerMeterBean.onEdit() {
        return null;
    }
    
    public boolean PowerMeterBean.isCreateDialogVisible() {
        return createDialogVisible;
    }
    
    public void PowerMeterBean.setCreateDialogVisible(boolean createDialogVisible) {
        this.createDialogVisible = createDialogVisible;
    }
    
    public String PowerMeterBean.displayList() {
        createDialogVisible = false;
        findAllPowerMeters();
        return "powerMeter";
    }
    
    public String PowerMeterBean.displayCreateDialog() {
        powerMeter = new PowerMeter();
        createDialogVisible = true;
        return "powerMeter";
    }
    
    public String PowerMeterBean.persist() {
        String message = "";
        if (powerMeter.getId() != null) {
            powerMeter.merge();
            message = "message_successfully_updated";
        } else {
            powerMeter.persist();
            message = "message_successfully_created";
        }
        RequestContext context = RequestContext.getCurrentInstance();
        context.execute("createDialogWidget.hide()");
        context.execute("editDialogWidget.hide()");
        
        FacesMessage facesMessage = MessageFactory.getMessage(message, "PowerMeter");
        FacesContext.getCurrentInstance().addMessage(null, facesMessage);
        reset();
        return findAllPowerMeters();
    }
    
    public String PowerMeterBean.delete() {
        powerMeter.remove();
        FacesMessage facesMessage = MessageFactory.getMessage("message_successfully_deleted", "PowerMeter");
        FacesContext.getCurrentInstance().addMessage(null, facesMessage);
        reset();
        return findAllPowerMeters();
    }
    
    public void PowerMeterBean.reset() {
        powerMeter = null;
        createDialogVisible = false;
    }
    
    public void PowerMeterBean.handleDialogClose(CloseEvent event) {
        reset();
    }
    
}