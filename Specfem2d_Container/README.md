### Installing Docker

Follow the guides for your operating system: https://www.docker.com  

### Running the Docker container

Open the terminal, and change directory to an empty working directory (e.g. specfem2d_container). We will need to mount our local filesystem, which will allow us saving the results we obtain from inside our container, in addition to sharing local folders/files to the container. 

```python
mkdir specfem2d_container
cd specfem2d_container
```
Then, copy the specfem2d DATA folder with the corresponding input files for your model (e.g., Par_File, STATIONS, SOURCES, interfaces.dat) into the working directory (specfem2d_container). 

To run the jupyter notebook example in the container, you can use the DATA folder in the GitHub repository (JupyterNotebooks/EXAMPLES). You need to copy DATA_Example01 to specfem2d_container and rename DATA_Example01 to DATA.

In addition, you can run your own models. Every time you use the command below to run the container, you must create a new working directory and copy the corresponding DATA folder. 

Then run the following docker run command:

#### Mac Intel, Windows, Linux 
```python
docker run -v ${PWD}:/notebooks --rm -p 8888:8888 arianoes/specfem2d_jn:amd64
```

#### Mac M1
```python
docker run -v ${PWD}:/notebooks --rm -p 8888:8888 arianoes/specfem2d_jn:arm64
```

Command Explanation:

- docker run: docker run command  
- -v ${PWD}:/notebooks binds current working directory (host) to container's /notebooks directory.  
- --rm removes container after shutdown (optional)  
- -p 8888:8888 bridges port 8888 between host and container. If your computer has some application using 8888 port it can be changed to another number (8889, 9000 e.g.).  
- arianoes/specfem2d_jn:arm64 docker image name that denotes username, image name and the version.  

Copy the last url printed to the terminal to your web browser window (it should look like: http://127.0.0.1:8888/lab?token=...).