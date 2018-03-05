title: Unit Testing example using Interfaces in Golang
date: 3/4/2018
details: A simple tutorial on writing unit tests with mocks in Golang.
post_no: 5

I recently started writing some code in Go (or Golang?) there are lot of amazing things to explore. Its always exciting to learn a new language.

So far, I absolutely love Golang. If you are like me who likes C, Python and all this systems/low level OS stuff, you'll get a feeling that Golang for systems will be similar to what JS is for the web.
(+ve JS things :-) ).

The example I take here is about unit testing an API which internally has some CRUD operation with a data store. The idea is to test the expected values to be
obtained from the API and mock out the backend data store interaction.

**Disclaimer: All the examples below are from my newbie Golang development experience. It may not be the best practise followed. But I would like to share whatever I learnt. :-P **

The Golang packages I am using are **Gorrila Mux** for the API and handlers, **Consul** for the backend state storage, **testify** with the default testing package for testing.

The main handler to be unit tested looks something like the following which has some Consul interaction which needs to be mocked during testing.

    func HandleGETS(w http.ResponseWriter, r *http.Request) {

        values, err := Consul.RequestGETS()         // Consul interaction which needs to be mocked.

        if err != nil {
            req := ResponseStruct{Response: string(err.Error())}
            w.Header().Set("Content-Type", "application/json")
            w.WriteHeader(http.StatusBadRequest)
            json.NewEncoder(w).Encode(req)
        } else {
            req := ResponseStruct{Response: values}
            w.Header().Set("Content-Type", "application/json")
            json.NewEncoder(w).Encode(req)
        }
    }

The call `Consul.RequestGETS()` needs to be mocked so that it doesn't call the actual Consul server. So to help with this, `Consul` is declared as an Interface.

    // Interface to have all Consul operation methods.
    type ConsulRequester interface {
        RequestPUT(string, string) error
        RequestGET(string) (string, error)
        RequestGETS() ([]string, error)         // <- We'll be mocking this method.
        RequestDELETE(string) error
    }

A struct implementing this interface is defined and the interface is initialized.

    type ConsulStruct struct {
        consulClient *consulapi.Client
    }

    var Consul ConsulRequester // var 'Consul' is an interface of type ConsulRequester.

For the purpose of this tutorial, assume that the struct `ConsulStruct` implements all the methods of the interface so that when the real API is run, it does
the real backend Consul interactions.

Now to test this out, we'll create a fake Consul struct which implements the interface with all the necessary methods. But the methods does no real Consul
interaction but is just a dummy function.

    type FakeConsul struct {
	    ConsulStruct            // Declared this to satisfy the interface. Else, Go complains that we have not implemented all the methods.
    }

    func (f *FakeConsul) RequestGETS() ([]string, error) {      // This is our mocked RequestGETS() method.
        return []string{"key1", "key2"}, nil                    // We'll make it return whatever we want.
    }

    func (f *FakeConsul) RequestGET(key string) (string, error) {
        return key, nil
    }

    func (f *FakeConsul) RequestPUT(key string, value string) error {
        return nil
    }

    func (f *FakeConsul) RequestDELETE(key string) error {
        return nil
    }

To now actually run tests with this, we have the following test function which tests the above `HandleGETS()` handler.

    func TestHandleGETS(t *testing.T) {
        oldConsul := Consul      // Real Consul
        Consul = &FakeConsul{}   // This the var Consul we declared above. Go accepts this since the fake Consul implements all methods.
        defer func() { Consul = oldConsul }()

        request, _ := http.NewRequest("GET", "/v1/gets", nil)
        response := httptest.NewRecorder()
        RouterConsul().ServeHTTP(response, request)
        expected := [2]string{"key1", "key2"}

        assert.Equal(t, expected, response.Body, "Response should be equal") // response.Body contains whatever wanted we wanted.
        assert.Equal(t, 200, response.Code, "200 response is expected")
    }

What we are doing here is, we initialize the `FakeConsul` struct to the `Consul` var. This is accepted since `FakeConsul` is implementing all the methods of
the Consul interface.

So now when the test is run, the `values, err := Consul.RequestGETS()` line in the handler code above runs on the `FakeConsul` and it runs the fake `RequestGETS()` we declared
above.This way, we can control whatever we want the `RequestGETS()` to return instead of actually running on Consul.

Hope the above example gives a good starting point in understanding unit testing in Golang using interfaces. It might be a bit confusing initially but look into it slowly
to understand.

## **Based on tutorials from:** ##

[https://husobee.github.io/golang/testing/unit-test/2015/06/08/golang-unit-testing.html](https://husobee.github.io/golang/testing/unit-test/2015/06/08/golang-unit-testing.html)

[https://nathanleclaire.com/blog/2015/10/10/interfaces-and-composition-for-effective-unit-testing-in-golang/](https://nathanleclaire.com/blog/2015/10/10/interfaces-and-composition-for-effective-unit-testing-in-golang/)