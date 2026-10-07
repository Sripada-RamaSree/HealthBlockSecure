package main
import (
 "encoding/json"
 "fmt"
 "time"
 "github.com/hyperledger/fabric-contract-api-go/contractapi"
)
type SmartContract struct{ contractapi.Contract }
type Record struct{ RecordID string `json:"record_id"`; PatientDID string `json:"patient_did"`; PolicyID string `json:"policy_id"`; StoragePointer string `json:"storage_pointer"`; RecordHash string `json:"record_hash"`; WrappedKey string `json:"wrapped_key"`; DataCategory string `json:"data_category"` }
type Policy struct{ PolicyID string `json:"policy_id"`; AllowedRoles []string `json:"allowed_roles"`; AllowedActions []string `json:"allowed_actions"`; StartHour int `json:"start_hour"`; EndHour int `json:"end_hour"` }
type Audit struct{ EventID string `json:"event_id"`; EventType string `json:"event_type"`; Timestamp string `json:"timestamp"`; Payload string `json:"payload"` }
func (s *SmartContract) PutRecord(ctx contractapi.TransactionContextInterface, id, payload string) error { var r Record; if err:=json.Unmarshal([]byte(payload),&r);err!=nil{return err}; if r.RecordID!=id{return fmt.Errorf("record id mismatch")}; b,_:=json.Marshal(r); return ctx.GetStub().PutState("REC_"+id,b) }
func (s *SmartContract) GetRecord(ctx contractapi.TransactionContextInterface,id string)(string,error){b,e:=ctx.GetStub().GetState("REC_"+id); if e!=nil||b==nil{return "",fmt.Errorf("record not found")};return string(b),nil}
func (s *SmartContract) PutPolicy(ctx contractapi.TransactionContextInterface,id,payload string) error {var p Policy;if err:=json.Unmarshal([]byte(payload),&p);err!=nil{return err};b,_:=json.Marshal(p);return ctx.GetStub().PutState("POL_"+id,b)}
func (s *SmartContract) GetPolicy(ctx contractapi.TransactionContextInterface,id string)(string,error){b,e:=ctx.GetStub().GetState("POL_"+id);if e!=nil||b==nil{return "",fmt.Errorf("policy not found")};return string(b),nil}
func (s *SmartContract) SetConsent(ctx contractapi.TransactionContextInterface,patient,record,grantee string,valid bool) error {key:="CON_"+patient+"_"+record+"_"+grantee;b,_:=json.Marshal(map[string]any{"valid":valid});return ctx.GetStub().PutState(key,b)}
func (s *SmartContract) LogAudit(ctx contractapi.TransactionContextInterface,eventID,eventType,payload string) error {a:=Audit{eventID,eventType,time.Now().UTC().Format(time.RFC3339Nano),payload};b,_:=json.Marshal(a);return ctx.GetStub().PutState("AUD_"+eventID,b)}
func main(){cc,err:=contractapi.NewChaincode(new(SmartContract));if err!=nil{panic(err)};if err:=cc.Start();err!=nil{panic(err)}}
