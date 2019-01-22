package hdfs.test;

import org.apache.hadoop.fs.FileStatus;
import org.apache.hadoop.fs.FileSystem;
import org.apache.hadoop.fs.Path;

import java.io.BufferedInputStream;
import java.io.ByteArrayInputStream;
import java.io.ByteArrayOutputStream;
import java.io.InputStream;

/**
 * Created by xiaoweiliang on 2019/1/17.
 */
public class CatFile {


    public static void main( String[] args ) throws Exception
    {
        if(args.length < 1){
            System.out.println("Invalid file name");
            return;
        }
        String fileName = args[0];
        FileSystem fs = FileSystem.get(Config.getHdfsConfig());
        if(!fs.exists(new Path(fileName))){
            System.out.println(fileName + " Not found!!!");
            return;
        }
        System.out.println("==========  File Content Begin:" + fileName + "  =============");
        InputStream in = fs.open(new Path(fileName));
        BufferedInputStream bis = new BufferedInputStream(in);
        ByteArrayOutputStream buf = new ByteArrayOutputStream();
        int result = bis.read();
        while(result != -1) {
            buf.write((byte) result);
            result = bis.read();
        }
        String str = buf.toString();
        System.out.println(str);
        fs.close();
        System.out.println(">>>>>>>>>>>>  File Content End:" + fileName + " <<<<<<<<<<<");
    }

}
