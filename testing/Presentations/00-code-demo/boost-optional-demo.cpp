// #> Preamble
#include<iostream>
#include<boost/optional.hpp>
#include<boost/optional/optional_io.hpp>

using namespace boost;

optional<double> calculate( double x )
{
  if( x > 10 )
    return 10*x;
}

// #<
int main(int argc, char *argv[])
{

  std::cout << "#>Usage\n";
  auto y = calculate( 5 );
  auto z = calculate( 15 );

  std::cout << "y: " << y << std::endl;
  std::cout << "z: " << z << std::endl;
  std::cout << "#<";

  return 0;
}
