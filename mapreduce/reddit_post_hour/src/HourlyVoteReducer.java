import java.io.IOException;

import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.io.IntWritable; 
import org.apache.hadoop.io.FloatWritable; 
import org.apache.hadoop.io.ArrayWritable; 
import org.apache.hadoop.io.Writable; 
import org.apache.hadoop.io.Text;

public class HourlyVoteCountReducer extends Reducer<Text, IntWritable, Text, FloatWritable> {

    @Override
    public void reduce(Text key, Iterable<IntWritable> values, Context context) 
        throws IOException, InterruptedException {
        int sum = 0;
        int n = 0;
        for (IntWritable val : values) {
            sum += val.get();
            n++;
        }
        float average = (float)sum / (float)n;
        context.write(key, new FloatWritable(average));
    }
}
