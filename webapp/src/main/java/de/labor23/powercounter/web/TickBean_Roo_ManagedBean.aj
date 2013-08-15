// WARNING: DO NOT EDIT THIS FILE. THIS FILE IS MANAGED BY SPRING ROO.
// You may push code into the target .java compilation unit if you wish to edit any member(s).

package de.labor23.powercounter.web;

import de.labor23.powercounter.dm.PowerMeter;
import de.labor23.powercounter.dm.Tick;
import de.labor23.powercounter.web.TickBean;
import de.labor23.powercounter.web.converter.PowerMeterConverter;
import de.labor23.powercounter.web.util.MessageFactory;
import java.util.ArrayList;
import java.util.Date;
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
import javax.faces.convert.DateTimeConverter;
import org.primefaces.component.autocomplete.AutoComplete;
import org.primefaces.component.calendar.Calendar;
import org.primefaces.component.message.Message;
import org.primefaces.component.outputlabel.OutputLabel;
import org.primefaces.context.RequestContext;
import org.primefaces.event.CloseEvent;

privileged aspect TickBean_Roo_ManagedBean {
    
    declare @type: TickBean: @ManagedBean(name = "tickBean");
    
    declare @type: TickBean: @SessionScoped;
    
    private String TickBean.name = "Ticks";
    
    private Tick TickBean.tick;
    
    private List<Tick> TickBean.allTicks;
    
    private boolean TickBean.dataVisible = false;
    
    private List<String> TickBean.columns;
    
    private HtmlPanelGrid TickBean.createPanelGrid;
    
    private HtmlPanelGrid TickBean.editPanelGrid;
    
    private HtmlPanelGrid TickBean.viewPanelGrid;
    
    private boolean TickBean.createDialogVisible = false;
    
    @PostConstruct
    public void TickBean.init() {
        columns = new ArrayList<String>();
        columns.add("occurence");
    }
    
    public String TickBean.getName() {
        return name;
    }
    
    public List<String> TickBean.getColumns() {
        return columns;
    }
    
    public List<Tick> TickBean.getAllTicks() {
        return allTicks;
    }
    
    public void TickBean.setAllTicks(List<Tick> allTicks) {
        this.allTicks = allTicks;
    }
    
    public String TickBean.findAllTicks() {
        allTicks = Tick.findAllTicks();
        dataVisible = !allTicks.isEmpty();
        return null;
    }
    
    public boolean TickBean.isDataVisible() {
        return dataVisible;
    }
    
    public void TickBean.setDataVisible(boolean dataVisible) {
        this.dataVisible = dataVisible;
    }
    
    public HtmlPanelGrid TickBean.getCreatePanelGrid() {
        if (createPanelGrid == null) {
            createPanelGrid = populateCreatePanel();
        }
        return createPanelGrid;
    }
    
    public void TickBean.setCreatePanelGrid(HtmlPanelGrid createPanelGrid) {
        this.createPanelGrid = createPanelGrid;
    }
    
    public HtmlPanelGrid TickBean.getEditPanelGrid() {
        if (editPanelGrid == null) {
            editPanelGrid = populateEditPanel();
        }
        return editPanelGrid;
    }
    
    public void TickBean.setEditPanelGrid(HtmlPanelGrid editPanelGrid) {
        this.editPanelGrid = editPanelGrid;
    }
    
    public HtmlPanelGrid TickBean.getViewPanelGrid() {
        return populateViewPanel();
    }
    
    public void TickBean.setViewPanelGrid(HtmlPanelGrid viewPanelGrid) {
        this.viewPanelGrid = viewPanelGrid;
    }
    
    public HtmlPanelGrid TickBean.populateCreatePanel() {
        FacesContext facesContext = FacesContext.getCurrentInstance();
        javax.faces.application.Application application = facesContext.getApplication();
        ExpressionFactory expressionFactory = application.getExpressionFactory();
        ELContext elContext = facesContext.getELContext();
        
        HtmlPanelGrid htmlPanelGrid = (HtmlPanelGrid) application.createComponent(HtmlPanelGrid.COMPONENT_TYPE);
        
        OutputLabel occurenceCreateOutput = (OutputLabel) application.createComponent(OutputLabel.COMPONENT_TYPE);
        occurenceCreateOutput.setFor("occurenceCreateInput");
        occurenceCreateOutput.setId("occurenceCreateOutput");
        occurenceCreateOutput.setValue("Occurence:");
        htmlPanelGrid.getChildren().add(occurenceCreateOutput);
        
        Calendar occurenceCreateInput = (Calendar) application.createComponent(Calendar.COMPONENT_TYPE);
        occurenceCreateInput.setId("occurenceCreateInput");
        occurenceCreateInput.setValueExpression("value", expressionFactory.createValueExpression(elContext, "#{tickBean.tick.occurence}", Date.class));
        occurenceCreateInput.setNavigator(true);
        occurenceCreateInput.setEffect("slideDown");
        occurenceCreateInput.setPattern("dd/MM/yyyy");
        occurenceCreateInput.setRequired(true);
        htmlPanelGrid.getChildren().add(occurenceCreateInput);
        
        Message occurenceCreateInputMessage = (Message) application.createComponent(Message.COMPONENT_TYPE);
        occurenceCreateInputMessage.setId("occurenceCreateInputMessage");
        occurenceCreateInputMessage.setFor("occurenceCreateInput");
        occurenceCreateInputMessage.setDisplay("icon");
        htmlPanelGrid.getChildren().add(occurenceCreateInputMessage);
        
        OutputLabel meterCreateOutput = (OutputLabel) application.createComponent(OutputLabel.COMPONENT_TYPE);
        meterCreateOutput.setFor("meterCreateInput");
        meterCreateOutput.setId("meterCreateOutput");
        meterCreateOutput.setValue("Meter:");
        htmlPanelGrid.getChildren().add(meterCreateOutput);
        
        AutoComplete meterCreateInput = (AutoComplete) application.createComponent(AutoComplete.COMPONENT_TYPE);
        meterCreateInput.setId("meterCreateInput");
        meterCreateInput.setValueExpression("value", expressionFactory.createValueExpression(elContext, "#{tickBean.tick.meter}", PowerMeter.class));
        meterCreateInput.setCompleteMethod(expressionFactory.createMethodExpression(elContext, "#{tickBean.completeMeter}", List.class, new Class[] { String.class }));
        meterCreateInput.setDropdown(true);
        meterCreateInput.setValueExpression("var", expressionFactory.createValueExpression(elContext, "meter", String.class));
        meterCreateInput.setValueExpression("itemLabel", expressionFactory.createValueExpression(elContext, "#{meter.meterName}", String.class));
        meterCreateInput.setValueExpression("itemValue", expressionFactory.createValueExpression(elContext, "#{meter}", PowerMeter.class));
        meterCreateInput.setConverter(new PowerMeterConverter());
        meterCreateInput.setRequired(true);
        htmlPanelGrid.getChildren().add(meterCreateInput);
        
        Message meterCreateInputMessage = (Message) application.createComponent(Message.COMPONENT_TYPE);
        meterCreateInputMessage.setId("meterCreateInputMessage");
        meterCreateInputMessage.setFor("meterCreateInput");
        meterCreateInputMessage.setDisplay("icon");
        htmlPanelGrid.getChildren().add(meterCreateInputMessage);
        
        return htmlPanelGrid;
    }
    
    public HtmlPanelGrid TickBean.populateEditPanel() {
        FacesContext facesContext = FacesContext.getCurrentInstance();
        javax.faces.application.Application application = facesContext.getApplication();
        ExpressionFactory expressionFactory = application.getExpressionFactory();
        ELContext elContext = facesContext.getELContext();
        
        HtmlPanelGrid htmlPanelGrid = (HtmlPanelGrid) application.createComponent(HtmlPanelGrid.COMPONENT_TYPE);
        
        OutputLabel occurenceEditOutput = (OutputLabel) application.createComponent(OutputLabel.COMPONENT_TYPE);
        occurenceEditOutput.setFor("occurenceEditInput");
        occurenceEditOutput.setId("occurenceEditOutput");
        occurenceEditOutput.setValue("Occurence:");
        htmlPanelGrid.getChildren().add(occurenceEditOutput);
        
        Calendar occurenceEditInput = (Calendar) application.createComponent(Calendar.COMPONENT_TYPE);
        occurenceEditInput.setId("occurenceEditInput");
        occurenceEditInput.setValueExpression("value", expressionFactory.createValueExpression(elContext, "#{tickBean.tick.occurence}", Date.class));
        occurenceEditInput.setNavigator(true);
        occurenceEditInput.setEffect("slideDown");
        occurenceEditInput.setPattern("dd/MM/yyyy");
        occurenceEditInput.setRequired(true);
        htmlPanelGrid.getChildren().add(occurenceEditInput);
        
        Message occurenceEditInputMessage = (Message) application.createComponent(Message.COMPONENT_TYPE);
        occurenceEditInputMessage.setId("occurenceEditInputMessage");
        occurenceEditInputMessage.setFor("occurenceEditInput");
        occurenceEditInputMessage.setDisplay("icon");
        htmlPanelGrid.getChildren().add(occurenceEditInputMessage);
        
        OutputLabel meterEditOutput = (OutputLabel) application.createComponent(OutputLabel.COMPONENT_TYPE);
        meterEditOutput.setFor("meterEditInput");
        meterEditOutput.setId("meterEditOutput");
        meterEditOutput.setValue("Meter:");
        htmlPanelGrid.getChildren().add(meterEditOutput);
        
        AutoComplete meterEditInput = (AutoComplete) application.createComponent(AutoComplete.COMPONENT_TYPE);
        meterEditInput.setId("meterEditInput");
        meterEditInput.setValueExpression("value", expressionFactory.createValueExpression(elContext, "#{tickBean.tick.meter}", PowerMeter.class));
        meterEditInput.setCompleteMethod(expressionFactory.createMethodExpression(elContext, "#{tickBean.completeMeter}", List.class, new Class[] { String.class }));
        meterEditInput.setDropdown(true);
        meterEditInput.setValueExpression("var", expressionFactory.createValueExpression(elContext, "meter", String.class));
        meterEditInput.setValueExpression("itemLabel", expressionFactory.createValueExpression(elContext, "#{meter.meterName}", String.class));
        meterEditInput.setValueExpression("itemValue", expressionFactory.createValueExpression(elContext, "#{meter}", PowerMeter.class));
        meterEditInput.setConverter(new PowerMeterConverter());
        meterEditInput.setRequired(true);
        htmlPanelGrid.getChildren().add(meterEditInput);
        
        Message meterEditInputMessage = (Message) application.createComponent(Message.COMPONENT_TYPE);
        meterEditInputMessage.setId("meterEditInputMessage");
        meterEditInputMessage.setFor("meterEditInput");
        meterEditInputMessage.setDisplay("icon");
        htmlPanelGrid.getChildren().add(meterEditInputMessage);
        
        return htmlPanelGrid;
    }
    
    public HtmlPanelGrid TickBean.populateViewPanel() {
        FacesContext facesContext = FacesContext.getCurrentInstance();
        javax.faces.application.Application application = facesContext.getApplication();
        ExpressionFactory expressionFactory = application.getExpressionFactory();
        ELContext elContext = facesContext.getELContext();
        
        HtmlPanelGrid htmlPanelGrid = (HtmlPanelGrid) application.createComponent(HtmlPanelGrid.COMPONENT_TYPE);
        
        HtmlOutputText occurenceLabel = (HtmlOutputText) application.createComponent(HtmlOutputText.COMPONENT_TYPE);
        occurenceLabel.setId("occurenceLabel");
        occurenceLabel.setValue("Occurence:");
        htmlPanelGrid.getChildren().add(occurenceLabel);
        
        HtmlOutputText occurenceValue = (HtmlOutputText) application.createComponent(HtmlOutputText.COMPONENT_TYPE);
        occurenceValue.setValueExpression("value", expressionFactory.createValueExpression(elContext, "#{tickBean.tick.occurence}", Date.class));
        DateTimeConverter occurenceValueConverter = (DateTimeConverter) application.createConverter(DateTimeConverter.CONVERTER_ID);
        occurenceValueConverter.setPattern("dd/MM/yyyy");
        occurenceValue.setConverter(occurenceValueConverter);
        htmlPanelGrid.getChildren().add(occurenceValue);
        
        HtmlOutputText meterLabel = (HtmlOutputText) application.createComponent(HtmlOutputText.COMPONENT_TYPE);
        meterLabel.setId("meterLabel");
        meterLabel.setValue("Meter:");
        htmlPanelGrid.getChildren().add(meterLabel);
        
        HtmlOutputText meterValue = (HtmlOutputText) application.createComponent(HtmlOutputText.COMPONENT_TYPE);
        meterValue.setValueExpression("value", expressionFactory.createValueExpression(elContext, "#{tickBean.tick.meter}", PowerMeter.class));
        meterValue.setConverter(new PowerMeterConverter());
        htmlPanelGrid.getChildren().add(meterValue);
        
        return htmlPanelGrid;
    }
    
    public Tick TickBean.getTick() {
        if (tick == null) {
            tick = new Tick();
        }
        return tick;
    }
    
    public void TickBean.setTick(Tick tick) {
        this.tick = tick;
    }
    
    public List<PowerMeter> TickBean.completeMeter(String query) {
        List<PowerMeter> suggestions = new ArrayList<PowerMeter>();
        for (PowerMeter powerMeter : PowerMeter.findAllPowerMeters()) {
            String powerMeterStr = String.valueOf(powerMeter.getMeterName());
            if (powerMeterStr.toLowerCase().startsWith(query.toLowerCase())) {
                suggestions.add(powerMeter);
            }
        }
        return suggestions;
    }
    
    public String TickBean.onEdit() {
        return null;
    }
    
    public boolean TickBean.isCreateDialogVisible() {
        return createDialogVisible;
    }
    
    public void TickBean.setCreateDialogVisible(boolean createDialogVisible) {
        this.createDialogVisible = createDialogVisible;
    }
    
    public String TickBean.displayList() {
        createDialogVisible = false;
        findAllTicks();
        return "tick";
    }
    
    public String TickBean.displayCreateDialog() {
        tick = new Tick();
        createDialogVisible = true;
        return "tick";
    }
    
    public String TickBean.persist() {
        String message = "";
        if (tick.getId() != null) {
            tick.merge();
            message = "message_successfully_updated";
        } else {
            tick.persist();
            message = "message_successfully_created";
        }
        RequestContext context = RequestContext.getCurrentInstance();
        context.execute("createDialogWidget.hide()");
        context.execute("editDialogWidget.hide()");
        
        FacesMessage facesMessage = MessageFactory.getMessage(message, "Tick");
        FacesContext.getCurrentInstance().addMessage(null, facesMessage);
        reset();
        return findAllTicks();
    }
    
    public String TickBean.delete() {
        tick.remove();
        FacesMessage facesMessage = MessageFactory.getMessage("message_successfully_deleted", "Tick");
        FacesContext.getCurrentInstance().addMessage(null, facesMessage);
        reset();
        return findAllTicks();
    }
    
    public void TickBean.reset() {
        tick = null;
        createDialogVisible = false;
    }
    
    public void TickBean.handleDialogClose(CloseEvent event) {
        reset();
    }
    
}
