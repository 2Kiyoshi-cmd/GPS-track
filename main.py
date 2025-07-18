from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from jnius import autoclass
from android import mActivity


class GPSApp(App):
    def build(self):
        self.label = Label(text="📡 Initializing GPS...", font_size='18sp')
        self.layout = BoxLayout(orientation='vertical')
        self.layout.add_widget(self.label)
        Clock.schedule_once(self.start_gps, 2)
        return self.layout

    def start_gps(self, dt):
        try:
            Context = autoclass('android.content.Context')
            LocationManager = autoclass('android.location.LocationManager')
            Criteria = autoclass('android.location.Criteria')
            criteria = Criteria()
            criteria.setAccuracy(Criteria.ACCURACY_FINE)
            criteria.setAltitudeRequired(True)
            criteria.setSpeedRequired(True)

            self.location_service = mActivity.getSystemService(Context.LOCATION_SERVICE)
            self.provider = self.location_service.getBestProvider(criteria, True)

            if not self.provider:
                self.label.text = "⚠️ GPS Provider not available"
                return

            Clock.schedule_interval(self.update_location, 2)

        except Exception as e:
            self.label.text = f"Error: {str(e)}"

    def update_location(self, dt):
        location = self.location_service.getLastKnownLocation(self.provider)
        if location:
            lat = location.getLatitude()
            lon = location.getLongitude()
            alt = location.getAltitude()
            acc = location.getAccuracy()
            spd = location.getSpeed()

            self.label.text = (
                f"🌍 Latitude:  {lat:.6f}\n"
                f"🌍 Longitude: {lon:.6f}\n"
                f"⬆️ Altitude:  {alt:.2f} m\n"
                f"🎯 Accuracy: ±{acc:.2f} m\n"
                f"🏃 Speed:    {spd:.2f} m/s"
            )
        else:
            self.label.text = "📡 Waiting for GPS fix..."


if __name__ == "__main__":
    GPSApp().run()
