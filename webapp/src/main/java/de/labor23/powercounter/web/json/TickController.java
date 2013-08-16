package de.labor23.powercounter.web.json;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.roo.addon.web.mvc.controller.json.RooWebJson;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.ResponseBody;

import de.labor23.powercounter.dm.Tick;
import de.labor23.powercounter.dm.json.TickDTO;

@RooWebJson(jsonObject = TickDTO.class)
@Controller
@RequestMapping("/tick")
public class TickController {
	
    @RequestMapping(method = RequestMethod.POST, headers = "Accept=application/json")
    public ResponseEntity<String> createFromJson(@RequestBody String json) {
    	String str = new String("{address:35,bank:0,occurence:1376673039966}");
        TickDTO tickDTO = TickDTO.fromJsonToTickDTO(str);
        System.out.println(tickDTO);
        Tick t = new Tick(tickDTO);
        t.persist();
        HttpHeaders headers = new HttpHeaders();
        headers.add("Content-Type", "application/json");
        return new ResponseEntity<String>(headers, HttpStatus.CREATED);
    }
    
    @RequestMapping(headers = "Accept=application/json")
    @ResponseBody
    public ResponseEntity<String> exampleJson() {
        TickDTO tickDTO = new TickDTO();
        HttpHeaders headers = new HttpHeaders();
        headers.add("Content-Type", "application/json; charset=utf-8");
        if (tickDTO == null) {
            return new ResponseEntity<String>(headers, HttpStatus.NOT_FOUND);
        }
        tickDTO.setAddress((byte) 0x23);
        tickDTO.setBank(0);
        return new ResponseEntity<String>(tickDTO.toJson(), headers, HttpStatus.OK);
    }
    
	/* Savings from roo
    @RequestMapping(value = "/{id}", method = RequestMethod.GET, headers = "Accept=application/json")
    @ResponseBody
    public ResponseEntity<String> TickController.showJson(@PathVariable("id") Long id) {
        TickDTO tickDTO = TickDTO.findTickDTO(id);
        HttpHeaders headers = new HttpHeaders();
        headers.add("Content-Type", "application/json; charset=utf-8");
        if (tickDTO == null) {
            return new ResponseEntity<String>(headers, HttpStatus.NOT_FOUND);
        }
        return new ResponseEntity<String>(tickDTO.toJson(), headers, HttpStatus.OK);
    }
    
    @RequestMapping(headers = "Accept=application/json")
    @ResponseBody
    public ResponseEntity<String> TickController.listJson() {
        HttpHeaders headers = new HttpHeaders();
        headers.add("Content-Type", "application/json; charset=utf-8");
        List<TickDTO> result = TickDTO.findAllTickDTO();
        return new ResponseEntity<String>(TickDTO.toJsonArray(result), headers, HttpStatus.OK);
    }
    
    @RequestMapping(method = RequestMethod.POST, headers = "Accept=application/json")
    public ResponseEntity<String> TickController.createFromJson(@RequestBody String json) {
        TickDTO tickDTO = TickDTO.fromJsonToTickDTO(json);
        tickDTO.persist();
        HttpHeaders headers = new HttpHeaders();
        headers.add("Content-Type", "application/json");
        return new ResponseEntity<String>(headers, HttpStatus.CREATED);
    }
    
    @RequestMapping(value = "/jsonArray", method = RequestMethod.POST, headers = "Accept=application/json")
    public ResponseEntity<String> TickController.createFromJsonArray(@RequestBody String json) {
        for (TickDTO tickDTO: TickDTO.fromJsonArrayToTickDTO(json)) {
            tickDTO.persist();
        }
        HttpHeaders headers = new HttpHeaders();
        headers.add("Content-Type", "application/json");
        return new ResponseEntity<String>(headers, HttpStatus.CREATED);
    }
    
    @RequestMapping(value = "/{id}", method = RequestMethod.PUT, headers = "Accept=application/json")
    public ResponseEntity<String> TickController.updateFromJson(@RequestBody String json, @PathVariable("id") Long id) {
        HttpHeaders headers = new HttpHeaders();
        headers.add("Content-Type", "application/json");
        TickDTO tickDTO = TickDTO.fromJsonToTickDTO(json);
        if (tickDTO.merge() == null) {
            return new ResponseEntity<String>(headers, HttpStatus.NOT_FOUND);
        }
        return new ResponseEntity<String>(headers, HttpStatus.OK);
    }
    
    @RequestMapping(value = "/{id}", method = RequestMethod.DELETE, headers = "Accept=application/json")
    public ResponseEntity<String> TickController.deleteFromJson(@PathVariable("id") Long id) {
        TickDTO tickDTO = TickDTO.findTickDTO(id);
        HttpHeaders headers = new HttpHeaders();
        headers.add("Content-Type", "application/json");
        if (tickDTO == null) {
            return new ResponseEntity<String>(headers, HttpStatus.NOT_FOUND);
        }
        tickDTO.remove();
        return new ResponseEntity<String>(headers, HttpStatus.OK);
    }
    */
}
