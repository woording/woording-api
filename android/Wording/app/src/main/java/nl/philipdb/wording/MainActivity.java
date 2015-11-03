package nl.philipdb.wording;

import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.support.v7.widget.LinearLayoutManager;
import android.support.v7.widget.RecyclerView;
import android.util.Log;
import android.view.Menu;
import android.view.MenuItem;
import android.support.v7.widget.Toolbar;

import org.json.JSONObject;

import java.util.ArrayList;

public class MainActivity extends AppCompatActivity {

    public static String username;

    private Toolbar mToolbar;
    private RecyclerView mRecyclerView;

    private static ListsViewAdapter mListsViewAdapter;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        // Setup toolbar
        mToolbar = (Toolbar) findViewById(R.id.toolbar);
        setSupportActionBar(mToolbar);

        // Setup RecyclerView
        mRecyclerView = (RecyclerView) findViewById(R.id.lists_view);
        // Setup LinearLayoutManager
        LinearLayoutManager linearLayoutManager = new LinearLayoutManager(this);
        mRecyclerView.setLayoutManager(linearLayoutManager);
        // Setup RecyclerView Adapter
        mListsViewAdapter = new ListsViewAdapter(new ArrayList<List>());
        mRecyclerView.setAdapter(mListsViewAdapter);

        // TODO: Only start login intent when not logged in
        Intent loginIntent = new Intent(this, LoginActivity.class);
        startActivity(loginIntent);
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.menu_main, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        // Handle action bar item clicks here. The action bar will
        // automatically handle clicks on the Home/Up button, so long
        // as you specify a parent activity in AndroidManifest.xml.
        int id = item.getItemId();

        //noinspection SimplifiableIfStatement
        if (id == R.id.action_settings) {
            return true;
        }

        return super.onOptionsItemSelected(item);
    }

    public static void handleResponse(JSONObject response) {
        Log.d("HandleResponse", response.toString());
        try {
            // Get the token
            NetworkCaller.mToken = response.getString("token");
            // Get the lists and add them
            mListsViewAdapter.addItemsToList(NetworkCaller.getLists(username));
        } catch (Exception e) {
            Log.w("Exception", e.getMessage());
        }
    }
}
