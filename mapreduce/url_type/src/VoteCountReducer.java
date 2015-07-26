import java.io.IOException;

import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.io.IntWritable; 
import org.apache.hadoop.io.FloatWritable; 
import org.apache.hadoop.io.ArrayWritable; 
import org.apache.hadoop.io.Writable; 
import org.apache.hadoop.io.Text;

public class VoteCountReducer extends Reducer<IntWritable, IntWritable, IntWritable, FloatWritable> {

    @Override
    public void reduce(IntWritable key, Iterable<IntWritable> values, Context context) {
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