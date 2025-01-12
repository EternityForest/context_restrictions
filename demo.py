
import context_restrictions
import traceback

outer = context_restrictions.Context("outer", exclusive=True)
inner = context_restrictions.Context("inner", exclusive=True)

outer.opens_before(inner)

with outer:
    print("It works like a lock when you specify exclusive=True")


try:
    with inner:
        with outer:
            print("It won't get here because inner is before outer")
except Exception as e:
    print(e)
    traceback.print_exc()

with outer:
    with inner:
        print("It works when it's in the right order")

class Foo():
    @outer.object_session_entry_point
    def f(self, other: "Foo|None"=None):
        """This is an entry point decorator for a session,
        it opens a session unless one is already open.

        The session is locked to this object.  It would raise
        if we tried to call a sessoin function of another object
        even of the same class
        """
        print("foo")
        self.g()

        # This will not work
        if other:
            other.f()

    @outer.object_session_entry_point
    def g(self):
        print("g")
        self.h()

    @outer.object_session_required
    def h(self):
        """Requires the context to already be open"""
        print("h")


f1 = Foo()
f1.f()

try:
    f2 = Foo()
    f2.f(f1)
except Exception as e:
    print(e)
    traceback.print_exc()