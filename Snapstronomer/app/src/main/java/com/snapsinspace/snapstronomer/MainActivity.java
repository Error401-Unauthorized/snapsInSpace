package com.snapsinspace.snapstronomer;


import android.app.Activity;
import android.app.Notification;
import android.app.PendingIntent;
import android.content.ActivityNotFoundException;
import android.content.Context;
import android.content.Intent;
import android.content.res.Resources;
import android.location.Location;
import android.location.LocationManager;
import android.media.Image;
import android.os.Bundle;
import android.speech.RecognizerIntent;
import android.speech.tts.TextToSpeech;
import android.telephony.gsm.SmsManager;
import android.util.Log;
import android.view.View;
import android.view.inputmethod.InputMethodManager;
import android.widget.Button;
import android.widget.EditText;
import android.widget.GridLayout;
import android.widget.ImageButton;
import android.widget.TextView;
import android.widget.Toast;
import com.chaquo.python.*;
import com.chaquo.python.android.AndroidPlatform;
import com.chaquo.python.android.PyApplication;
import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.ByteArrayOutputStream;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileWriter;
import java.io.IOException;
import java.io.InputStream;
import java.io.PrintWriter;
import java.nio.file.FileSystems;
import java.util.ArrayList;
import java.util.Locale;
import java.net.*;


public class MainActivity extends Activity {
    private String outputFile;
    private String tleFile = "Snapstronomer\\app\\src\\main\\assets\\tle.txt";
    private String fontFile = "Snapstronomer\\app\\src\\main\\assets\\nasalization-rg.ttf";
    private String picFile = "Snapstronomer\\app\\src\\main\\assets\\BlankStamp2.png";
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        PyApplication p = new PyApplication();
        //Python py = Python.getInstance();
        //final PyObject goodStuff = py.getModule("bigpackage.bigpackage");

        setContentView(R.layout.activity_main);
        LocationManager locationManager = (LocationManager)getSystemService(Context.LOCATION_SERVICE);
        final MyCurrentLocationListener locationListener = new MyCurrentLocationListener();
        try {
            locationManager.requestLocationUpdates(LocationManager.GPS_PROVIDER, 0, 0, locationListener);
        }
        catch (SecurityException f) {
            Toast.makeText(getApplicationContext(), "Please enable location services for this app in your settings",Toast.LENGTH_LONG).show();
        }
        final Button searchButton = (Button)findViewById(R.id.searcher);
        final GridLayout sats = (GridLayout)findViewById(R.id.Satellites);
        searchButton.setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) {
                sats.setVisibility(View.VISIBLE);
                searchButton.setVisibility(View.INVISIBLE);
                double[] coord = locationListener.getCoord();

                ((Button)findViewById(R.id.Satellite1)).setMinimumHeight(((Button)findViewById(R.id.Satellite1)).getWidth()/2);
                ((Button)findViewById(R.id.Satellite1)).setText("Lat:  " + coord[0] + "\nLong: " + coord[1] + "\nAlt:" + coord[2]);
             //   PyObject ret = goodStuff.callAttr("funct", coord[0], coord[1], coord[2], fontFile, picFile);
               // String help = ret.toString();
                //System.out.println(help);
            }
        });
    }
}

class MyCurrentLocationListener implements android.location.LocationListener {
    double myLat = 0;
    double myLon = 0;
    double myAlt = 0;
    public double[] getCoord() {
        double[] retArr = {myLat, myLon, myAlt};
        return retArr;
    }

    @Override
    public void onLocationChanged(Location location) {
        myLat = location.getLatitude();
        myLon = location.getLongitude();
        myAlt = location.getAltitude();
        String myLocation = "Latitude = " + location.getLatitude() + " Longitude = " + location.getLongitude();

        //I make a log to see the results
        Log.e("MY CURRENT LOCATION", myLocation);
    }

    @Override
    public void onStatusChanged(String s, int i, Bundle bundle) {

    }

    @Override
    public void onProviderEnabled(String s) {

    }

    @Override
    public void onProviderDisabled(String s) {

    }
}
