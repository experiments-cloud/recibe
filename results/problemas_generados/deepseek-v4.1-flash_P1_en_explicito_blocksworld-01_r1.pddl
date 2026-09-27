(define (problem blocks-five)
  (:domain BLOCKS)
  (:objects
    a b c d e - block
  )
  (:init
    (ontable b)
    (on a b)
    (on c a)
    (on d e)
    (on e c)
    (clear d)
    (handempty)
  )
  (:goal (and
    (on b e)
    (on c b)
    (on d c)
    (on e a)
  ))
)
