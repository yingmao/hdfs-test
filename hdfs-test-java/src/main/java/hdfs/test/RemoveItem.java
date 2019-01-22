package hdfs.test;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.FileSystem;
import org.apache.hadoop.fs.Path;

public class RemoveItem {

    public static void main( String[] args ) throws Exception
    {
        if(args.length < 1){
            System.out.println("Invalid dir name");
            return;
        }
        String dirName = args[0];
        FileSystem fs = FileSystem.get(Config.getHdfsConfig());
        if(!fs.exists(new Path(dirName))){
            System.out.println(dirName + " Not found!!!");
            return;
        }
        fs.delete(new Path(dirName),true);
        fs.close();
        System.out.println("Remove file or dictionary success!");
    }

}
